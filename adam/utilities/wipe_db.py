import sys
import os

# Add the parent directory of 'adam' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from adam.database import db, ConversationModel, MessageModel

async def wipe_db(db):
    await db.init_db()

if __name__ == "__main__":
    import asyncio
    asyncio.run(wipe_db(db))