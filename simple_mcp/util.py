import json
import contextlib
from fastmcp.client.transports import PythonStdioTransport, SSETransport
from fastmcp import Client


class LoggingPythonStdioTransport(PythonStdioTransport):
    @contextlib.asynccontextmanager
    async def connect_session(self, **session_kwargs):
        async with super().connect_session(**session_kwargs) as session:
            orig_send = session._write_stream.send
            orig_receive = session._read_stream.receive

            async def send_wrapper(message):
                return await orig_send(message)

            async def receive_wrapper():
                return await orig_receive()

            session._write_stream.send = send_wrapper
            session._read_stream.receive = receive_wrapper
            yield session


class LoggingSSETransport(SSETransport):
    @contextlib.asynccontextmanager
    async def connect_session(self, **session_kwargs):
        async with super().connect_session(**session_kwargs) as session:
            orig_send = session._write_stream.send
            orig_receive = session._read_stream.receive

            async def send_wrapper(message):
                try:
                    raw = message.model_dump_json()
                except Exception:
                    raw = str(message)
                print("→ RAW Request JSON-RPC:", raw)
                return await orig_send(message)

            async def receive_wrapper():
                return await orig_receive()

            session._write_stream.send = send_wrapper
            session._read_stream.receive = receive_wrapper
            yield session


# Client.call_tool 로깅 패치: parsed 결과를 자동으로 출력하도록 오버라이드
orig_client_call_tool = Client.call_tool
async def logging_call_tool(self, name, arguments=None, _return_raw_result=False):
    # parsed request 로깅
    print(f"→ Parsed Request [{name}]:")
    if arguments is not None:
        print(json.dumps(arguments, indent=2, ensure_ascii=False))
    else:
        print("null")
    # raw JSON-RPC 응답을 항상 받아오기
    raw = await orig_client_call_tool(self, name, arguments, _return_raw_result=True)
    # raw JSON-RPC 응답 출력
    print("← RAW JSON-RPC 응답:")
    print(json.dumps(raw.model_dump(), indent=2, ensure_ascii=False))
    # _return_raw_result=True인 경우 raw 그대로 반환
    if _return_raw_result:
        return raw
    # parsed response content 로깅
    content = getattr(raw, 'content', None)
    print("← Parsed Response Content:")
    if isinstance(content, list):
        parsed_text = ''.join(getattr(item, 'text', str(item)) for item in content)
        print(parsed_text)
    else:
        print(content)
    # 기본 동작과 동일하게 parsed content 반환
    return raw.content
Client.call_tool = logging_call_tool


async def call_and_log(client: Client, tool_name: str, arguments: dict[str, any]):
    """call_tool 실행 후 raw JSON-RPC 요청/응답과 결과를 로그로 출력한다."""
    # 1) 원시 JSON-RPC 응답(raw CallToolResult) 수신
    raw = await client.call_tool(tool_name, arguments, _return_raw_result=True)
    # 2) raw JSON-RPC 응답 출력
    print("← RAW JSON-RPC 응답:")
    dump = raw.model_dump()
    print(json.dumps(dump, indent=2, ensure_ascii=False))
    # 3) 실제 텍스트 결과만 추출
    contents = dump.get('content', [])
    if isinstance(contents, list) and contents and isinstance(contents[0], dict) and 'text' in contents[0]:
        text_output = ''.join(item['text'] for item in contents)
    else:
        text_output = contents
    print(f"{tool_name} 결과: {text_output}")
    return text_output 