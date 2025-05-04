#!/usr/bin/env python3
from fastmcp import FastMCP

# Agent용 도구 서버: add, subtract 툴 제공
mcp = FastMCP("Agent Tool Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """첫 번째 숫자에서 두 번째 숫자를 뺍니다."""
    return a - b

if __name__ == "__main__":
    # 기본 STDIO 모드로 서버 실행
    mcp.run()
