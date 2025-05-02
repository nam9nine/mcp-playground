import asyncio
from fastmcp import Client
from util import LoggingPythonStdioTransport

async def main():
    # STDIO 모드: Logging transport이 요청/응답(raw+parsed)을 자동으로 로깅합니다
    transport = LoggingPythonStdioTransport("simple_stdio_server.py")
    async with Client(transport) as client:
        # add 툴 호출: raw request/response와 parsed response가 콘솔에 출력됩니다
        await client.call_tool("add", {"a": 3, "b": 4})

if __name__ == "__main__":
    asyncio.run(main())