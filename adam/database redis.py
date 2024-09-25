import json
from typing import Optional, List
from pydantic import BaseModel
import redis.asyncio as redis

class ConversationModel(BaseModel):
    id: Optional[int] = None
    conversation_name: Optional[str] = None
    subject: str
    rewritten_prompt: str
    meta_prompt_one: str
    meta_prompt_two: str

class MessageModel(BaseModel):
    id: Optional[int] = None
    conversation_id: int
    sender_name: str
    message: str
    type: str

class Database:
    def __init__(self, redis_url: str = 'redis://localhost'):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.conversation_key = "conversation:"
        self.message_key = "message:"
        self.conversation_id_key = "conversation_id"
        self.message_id_key = "message_id"
        self.conversation_index_key = "conversation_index"

    async def init_db(self):
        """Initialize the database by clearing all data."""
        await self.redis.flushdb()
        print("Database initialized and all data cleared.")

    async def add_conversation(self, conversation: ConversationModel) -> int:
        """Add a new conversation to the database."""
        conversation_id = await self.redis.incr(self.conversation_id_key)
        conversation.id = conversation_id
        await self.redis.hset(
            f"{self.conversation_key}{conversation_id}",
            mapping=conversation.dict()
        )
        await self.redis.sadd(self.conversation_index_key, conversation_id)
        return conversation_id

    async def add_message(self, message: MessageModel) -> int:
        """Add a new message to the database."""
        message_id = await self.redis.incr(self.message_id_key)
        message.id = message_id
        await self.redis.hset(
            f"{self.message_key}{message_id}",
            mapping=message.dict()
        )
        await self.redis.sadd(f"conversation:{message.conversation_id}:messages", message_id)
        return message_id

    async def get_conversations(self) -> List[ConversationModel]:
        """Retrieve all conversations from the database."""
        conversation_ids = await self.redis.smembers(self.conversation_index_key)
        conversations = []
        for conv_id in conversation_ids:
            conv_data = await self.redis.hgetall(f"{self.conversation_key}{conv_id}")
            if conv_data:
                conversations.append(ConversationModel(**conv_data))
        return conversations

    async def get_messages(self, conversation_id: int) -> List[MessageModel]:
        """Retrieve all messages for a specific conversation."""
        message_ids = await self.redis.smembers(f"conversation:{conversation_id}:messages")
        messages = []
        for msg_id in message_ids:
            msg_data = await self.redis.hgetall(f"{self.message_key}{msg_id}")
            if msg_data:
                messages.append(MessageModel(**msg_data))
        return sorted(messages, key=lambda x: x.id)

    async def delete_all_conversations(self):
        """Delete all conversations from the database."""
        conversation_ids = await self.redis.smembers(self.conversation_index_key)
        for conv_id in conversation_ids:
            await self.redis.delete(f"{self.conversation_key}{conv_id}")
            await self.redis.delete(f"conversation:{conv_id}:messages")
        await self.redis.delete(self.conversation_index_key)

    async def delete_all_messages(self):
        """Delete all messages from the database."""
        conversation_ids = await self.redis.smembers(self.conversation_index_key)
        for conv_id in conversation_ids:
            message_ids = await self.redis.smembers(f"conversation:{conv_id}:messages")
            for msg_id in message_ids:
                await self.redis.delete(f"{self.message_key}{msg_id}")
            await self.redis.delete(f"conversation:{conv_id}:messages")

    async def initialize_database(self):
        """Initialize the database with a default conversation and message."""
        await self.init_db()
        first_conversation = ConversationModel(
            subject="Initial Conversation",
            rewritten_prompt="Welcome to the conversation",
            meta_prompt_one="This is meta prompt one",
            meta_prompt_two="This is meta prompt two"
        )
        conv_id = await self.add_conversation(first_conversation)
        first_message = MessageModel(
            conversation_id=conv_id,
            sender_name="System",
            message="Conversation initialized and online.",
            type="outer"
        )
        await self.add_message(first_message)
        print(f"Initial conversation and message added to database")

    async def get_db_messages(self, conversation_id: int, after_id: int) -> List[MessageModel]:
        """Retrieve messages for a specific conversation after a given message ID."""
        message_ids = await self.redis.smembers(f"conversation:{conversation_id}:messages")
        messages = []
        for msg_id in message_ids:
            if int(msg_id) > after_id:
                msg_data = await self.redis.hgetall(f"{self.message_key}{msg_id}")
                if msg_data:
                    messages.append(MessageModel(**msg_data))
        return sorted(messages, key=lambda x: x.id)

    async def get_latest_conversation_id(self) -> Optional[int]:
        """Retrieve the ID of the most recently created conversation."""
        conversation_ids = await self.redis.smembers(self.conversation_index_key)
        if conversation_ids:
            return max(map(int, conversation_ids))
        return None

    async def get_last_user_message(self, conversation_id: int) -> Optional[MessageModel]:
        """Retrieve the last user message for a specific conversation."""
        message_ids = await self.redis.smembers(f"conversation:{conversation_id}:messages")
        user_messages = []
        for msg_id in message_ids:
            msg_data = await self.redis.hgetall(f"{self.message_key}{msg_id}")
            if msg_data and msg_data.get('sender_name') == 'User':
                user_messages.append(MessageModel(**msg_data))
        if user_messages:
            return max(user_messages, key=lambda x: x.id)
        return None

# Create a global instance of the Database class
db = Database()
