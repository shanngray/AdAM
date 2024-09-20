import sys
import os
import asyncio
import logging
import subprocess
import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv(override=True)

from adam.server import db, router, manager, handle_user_input
import tracemalloc

tracemalloc.start()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
# Suppress aiosqlite debug logs
logging.getLogger("aiosqlite").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.WARNING)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(router, prefix="/server") # may need to add a prefix i.e. "/test"

@app.on_event("startup")
async def startup_event():
    # This function will run when the FastAPI application starts
    loop = asyncio.get_running_loop()
    loop.set_debug(True)
    print("FastAPI application is starting up...")
    
    # You can add any other startup tasks here
    # For example:
    # task1 = asyncio.create_task(some_async_function())
    # task2 = asyncio.create_task(another_async_function())
    # await asyncio.gather(task1, task2)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("adam.main:app", host="0.0.0.0", port=8080, reload=True)
