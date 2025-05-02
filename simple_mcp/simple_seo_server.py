from fastmcp import FastMCP

# 1) FastMCP 인스턴스 생성 (이 단계에서는 host/port 지정 안 함)
mcp = FastMCP("Demo Server")

# 2) add 툴 등록
@mcp.tool()
def add(a: int, b: int) -> int:
    """두 숫자를 더해서 반환"""
    return a + b

if __name__ == "__main__":
    # 3) HTTP/SSE 모드로 실행, 127.0.0.1:8080에 리스닝
    mcp.run(
        transport="sse",         # Server-Sent Events 방식
        host="127.0.0.1",         # 바인딩할 호스트
        port=8080                # 열 포트 지정
    )
