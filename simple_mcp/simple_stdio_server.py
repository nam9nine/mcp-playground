from fastmcp import FastMCP

# 1) FastMCP 인스턴스 생성 (STDIO 모드 기본)
mcp = FastMCP("Demo Server")

# 2) add 툴 등록
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    # 3) transport 옵션 없이 run()만 호출하면 STDIO 모드로 실행
    mcp.run()
