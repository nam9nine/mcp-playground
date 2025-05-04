import os
import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.tool import ToolMessage

# OpenAI API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("환경변수 OPENAI_API_KEY를 설정해주세요.")

async def main():
    # MCP 서버 설정
    servers = {
        "toolserver": {
            "command": sys.executable,
            "args": ["mcp_server.py"],
            "transport": "stdio",
        }
    }

    # MultiServerMCPClient 사용
    async with MultiServerMCPClient(servers) as mcp_client:
        # MCP tools 로드
        tools = mcp_client.get_tools()

        # LangChain 모델 설정
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)

        # 시스템 메시지: 등록된 도구만 사용하고, 그 외 요청에는 툴 호출을 금지
        system_prompt = (
            "당신은 서버에 등록된 도구(add, subtract)만 사용할 수 있습니다. "
            "서버에 없는 기능이 요청된 경우 절대 도구를 호출하지 말고, '죄송합니다. 해당 기능을 지원하지 않습니다.'라고 응답하십시오."
        )
        # LangGraph React Agent 생성 (커스텀 시스템 메시지 포함)
        agent = create_react_agent(
            llm,
            tools,
            prompt=system_prompt
        )

        # 사용자에게 계산 요청 입력 받기
        user_query = input("계산할 내용을 입력하세요 (예: 3 더하기 5): ")
        # 비동기로 실행하여 응답 받기
        response = await agent.ainvoke({"messages": user_query})

        # 응답을 보기 좋게 포맷팅하고 툴 사용 여부 표시
        if isinstance(response, dict) and "messages" in response:
            print("=== 대화 로그 ===")
            tool_used = False
            tool_names: set[str] = set()
            for msg in response["messages"]:
                role = msg.__class__.__name__.replace("Message", "")
                content = getattr(msg, "content", str(msg))
                # 도구 호출 메시지는 ToolMessage로 처리
                if isinstance(msg, ToolMessage):
                    tool_used = True
                    tool_names.add(msg.name)
                    print(f"[Tool:{msg.name}] {content}")
                else:
                    # 빈 content인 중간 AIMessage는 생략
                    if content.strip():
                        print(f"[{role}] {content}")
            print()
            # 툴 사용 여부 및 사용한 툴 이름 출력
            if tool_used:
                print(f"툴 사용 여부: 사용함, 사용한 툴: {', '.join(tool_names)}")
            else:
                print("툴 사용 여부: 사용하지 않음")
        else:
            print("Agent 응답:", response)

if __name__ == '__main__':
    asyncio.run(main())
