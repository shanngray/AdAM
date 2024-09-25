from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Create a new conversation
new_conversation = Conversation(conversation_name="My First Conversation", subject="Test Subject")
session.add(new_conversation)
session.commit()

# Add a message to the conversation
new_message = Message(conversation_id=new_conversation.id, sender_name="Alice", message="Hello, world!", type="outer")
session.add(new_message)
session.commit()

# Query the database
conversations = session.query(Conversation).all()
for conv in conversations:
    print(f"Conversation: {conv.conversation_name}")
    for msg in conv.messages:
        print(f"  Message from {msg.sender_name}: {msg.message}")

session.close()
