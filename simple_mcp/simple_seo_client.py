import asyncio
from fastmcp import Client
from util import LoggingSSETransport

async def main():
    
    transport = LoggingSSETransport("http://127.0.0.1:8080/sse")

    async with Client(transport) as client:
        # add 툴 호출
        result = await client.call_tool("add", {"a": 5, "b": 7})
        print("5 + 7 =", result)  # → "5 + 7 = 12"

if __name__ == "__main__":
    asyncio.run(main())
