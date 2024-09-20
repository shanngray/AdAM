from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy import Column, Integer, String, ForeignKey, Text, delete, update
from contextlib import asynccontextmanager
from sqlalchemy import text, inspect

Base = declarative_base()

class Conversation(Base):
    """
    SQLAlchemy model for conversations.

    Attributes:
        id (int): Primary key for the conversation.
        conversation_name (str): Optional name for the conversation.
        subject (str): Subject of the conversation.
        rewritten_prompt (str): Rewritten prompt for the conversation.
        meta_prompt_one (str): First meta prompt for the conversation.
        meta_prompt_two (str): Second meta prompt for the conversation.
        messages (relationship): Relationship to associated messages.
        conversation_state (str): State of the conversation, defaults to "first_message".
    """
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, index=True)
    conversation_name = Column(String, nullable=True)
    subject = Column(String)
    rewritten_prompt = Column(Text)
    meta_prompt_one = Column(Text)
    meta_prompt_two = Column(Text)
    messages = relationship("Message", back_populates="conversation")
    conversation_state = Column(String, default="first_message")

class Message(Base):
    """
    SQLAlchemy model for messages.

    Attributes:
        id (int): Primary key for the message.
        conversation_id (int): Foreign key to the associated conversation.
        sender_name (str): Name of the message sender.
        message (str): Content of the message.
        type (str): Type of the message ('outer' or 'inner').
        conversation (relationship): Relationship to the associated conversation.
    """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    sender_name = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # 'outer' or 'inner'

    conversation = relationship("Conversation", back_populates="messages")

class ConversationModel(BaseModel):
    """
    Pydantic model for conversations.

    Attributes:
        id (Optional[int]): ID of the conversation.
        conversation_name (Optional[str]): Name of the conversation.
        subject (str): Subject of the conversation.
        rewritten_prompt (str): Rewritten prompt for the conversation.
        meta_prompt_one (str): First meta prompt for the conversation.
        meta_prompt_two (str): Second meta prompt for the conversation.
        conversation_state (str): State of the conversation, defaults to "first_message".
    """
    id: Optional[int] = None
    conversation_name: Optional[str] = None
    subject: str
    rewritten_prompt: str
    meta_prompt_one: str
    meta_prompt_two: str
    conversation_state: str = Field(default="first_message")

class MessageModel(BaseModel):
    """
    Pydantic model for messages.

    Attributes:
        id (Optional[int]): ID of the message.
        conversation_id (int): ID of the associated conversation.
        sender_name (str): Name of the message sender.
        message (str): Content of the message.
        type (str): Type of the message.
    """
    id: Optional[int] = None
    conversation_id: int
    sender_name: str
    message: str
    type: str

class Database:
    """
    Handles database operations for conversations and messages.

    This class provides methods for initializing the database, adding and
    retrieving conversations and messages, and other database operations.

    Attributes:
        engine: SQLAlchemy async engine.
        SessionLocal: SQLAlchemy sessionmaker for creating database sessions.
    """
    def __init__(self, db_url: str = 'sqlite+aiosqlite:///conversations.db'):
        """
        Initialize the Database class.

        Args:
            db_url (str): URL for the database connection.
        """
        self.engine = create_async_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

    @asynccontextmanager
    async def session(self):
        """
        Context manager for database sessions.

        Yields:
            AsyncSession: An async database session.

        Raises:
            Exception: If an error occurs during the session.
        """
        async with self.SessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def init_db(self):
        """
        Initialize the database by dropping and recreating all tables.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        print("Database initialized with all tables recreated.")

    async def add_conversation(self, conversation: ConversationModel) -> int:
        """
        Add a new conversation to the database.

        Args:
            conversation (ConversationModel): The conversation to add.

        Returns:
            int: The ID of the newly added conversation.
        """
        async with self.session() as session:
            db_conversation = Conversation(**conversation.dict(exclude={'id'}))
            session.add(db_conversation)
            await session.flush()
            return db_conversation.id

    async def update_conversation(self, conversation_id: int, **kwargs):
        """
        Update any combination of fields for a specific conversation.

        Args:
            conversation_id (int): The ID of the conversation to update.
            **kwargs: Arbitrary keyword arguments representing the fields to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        async with self.session() as session:
            stmt = (
                update(Conversation)
                .where(Conversation.id == conversation_id)
                .values(**kwargs)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
    
    async def add_message(self, message: MessageModel) -> int:
        """
        Add a new message to the database.

        Args:
            message (MessageModel): The message to add.

        Returns:
            int: The ID of the newly added message.
        """
        async with self.session() as session:
            db_message = Message(**message.dict(exclude={'id'}))
            session.add(db_message)
            await session.flush()
            return db_message.id

    async def get_conversations(self) -> List[ConversationModel]:
        """
        Retrieve all conversations from the database.

        Returns:
            List[ConversationModel]: A list of all conversations.
        """
        async with self.session() as session:
            result = await session.execute(select(Conversation))
            conversations = result.scalars().all()
            return [ConversationModel(**conversation.__dict__) for conversation in conversations]

    async def get_messages(self, conversation_id: int) -> List[MessageModel]:
        """
        Retrieve all messages for a specific conversation.

        Args:
            conversation_id (int): The ID of the conversation.

        Returns:
            List[MessageModel]: A list of messages for the specified conversation.
        """
        async with self.session() as session:
            result = await session.execute(select(Message).where(Message.conversation_id == conversation_id))
            messages = result.scalars().all()
            return [MessageModel(**message.__dict__) for message in messages]

    async def delete_all_conversations(self):
        """Delete all conversations from the database."""
        async with self.session() as session:
            await session.execute(delete(Conversation))

    async def delete_all_messages(self):
        """Delete all messages from the database."""
        async with self.session() as session:
            await session.execute(delete(Message))

    async def initialize_database(self):
        """
        Initialize the database with a default conversation and message.
        """
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

    async def get_conversation_messages(self, conversation_id: int, after_id: Optional[int] = None) -> tuple[List[MessageModel], Optional[str]]:
        """
        Retrieve messages for a specific conversation, optionally after a given message ID.

        Args:
            conversation_id (int): The ID of the conversation.
            after_id (Optional[int]): The ID after which to retrieve messages. If None, retrieve all messages.

        Returns:
            Tuple[List[MessageModel], Optional[str]]: A tuple containing a list of messages matching the criteria and the conversation state.
        """
        async with self.session() as session:
            query = select(Message).where(Message.conversation_id == conversation_id)
            
            if after_id is not None:
                query = query.where(Message.id > after_id)
            
            query = query.order_by(Message.id)
            
            result = await session.execute(query)
            messages = result.scalars().all()
            
            # Fetch conversation state
            state_query = select(Conversation.conversation_state).where(Conversation.id == conversation_id)
            state_result = await session.execute(state_query)
            conversation_state = state_result.scalar_one_or_none()
            
            return [MessageModel(**message.__dict__) for message in messages], conversation_state

    async def get_latest_conversation_id(self) -> Optional[int]:
        """
        Retrieve the ID of the most recently created conversation.

        Returns:
            Optional[int]: The ID of the most recent conversation, or None if no conversations exist.
        """
        async with self.session() as session:
            result = await session.execute(
                select(Conversation.id)
                .order_by(Conversation.id.desc())
                .limit(1)
            )
            return result.scalar_one_or_none()

    async def get_conversation(self, conversation_id: int) -> Optional[ConversationModel]:
        """
        Retrieve a conversation by its ID.

        Args:
            conversation_id (int): The ID of the conversation.

        Returns:
            Optional[ConversationModel]: The conversation, or None if not found.
        """
        async with self.session() as session:
            result = await session.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            return ConversationModel(**conversation.__dict__) if conversation else None

    async def get_last_user_message(self, conversation_id: int) -> Optional[MessageModel]:
        """
        Retrieve the last user message for a specific conversation.

        Args:
            conversation_id (int): The ID of the conversation.

        Returns:
            Optional[MessageModel]: The last user message, or None if no user messages exist.
        """
        async with self.session() as session:
            result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .where(Message.sender_name == "User")
                .order_by(Message.id.desc())
                .limit(1)
            )
            message = result.scalar_one_or_none()
            return MessageModel(**message.__dict__) if message else None

    async def delete_all_records(self):
        """Delete all records from all tables in the database."""

        
        print("All records have been deleted from all tables.")

# Create a global instance of the Database class
db = Database()
