import asyncio
import httpx

async def test_stream_endpoint():
    async with httpx.AsyncClient() as client:
        url = "http://localhost:8080/messages"  # Adjust the URL if needed
        params = {
            "chain": "your_chain_value",
            "input_data": "your_input_data"
        }
        async with client.stream("GET", url, params=params) as response:
            async for line in response.aiter_lines():
                print(line)

asyncio.run(test_stream_endpoint())
