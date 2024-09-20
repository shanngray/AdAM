import asyncio
import logging

# Set up logging to show detailed information
logging.basicConfig(level=logging.DEBUG)

async def worker_1(lock):
    logging.debug("Worker 1 trying to acquire the lock")
    async with lock:
        logging.debug("Worker 1 acquired the lock")
        await asyncio.sleep(2)  # Simulate work
        logging.debug("Worker 1 finished work and will release the lock")

async def worker_2(lock):
    logging.debug("Worker 2 trying to acquire the lock")
    await asyncio.sleep(1)  # Simulate work before acquiring lock
    async with lock:
        logging.debug("Worker 2 acquired the lock")
        await asyncio.sleep(2)  # Simulate work
        logging.debug("Worker 2 finished work and will release the lock")
'''
async def main():
    # Enable asyncio debugging
    loop = asyncio.get_running_loop()
    loop.set_debug(True)

    # Create a shared lock
    lock = asyncio.Lock()

    # Start workers that might deadlock
    await asyncio.gather(
        worker_1(lock),
        worker_2(lock)
    )
'''
async def main():
    loop = asyncio.get_running_loop()
    loop.set_debug(True)

    lock = asyncio.Lock()

    try:
        await asyncio.wait_for(
            asyncio.gather(worker_1(lock), worker_2(lock)),
            timeout=5  # Set timeout to prevent deadlock
        )
    except asyncio.TimeoutError:
        logging.error("Deadlock detected or task took too long!")

if __name__ == "__main__":
    # Enable asyncio debug through environment
    asyncio.run(main())