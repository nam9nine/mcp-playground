# MCP Agent 예제

이 프로젝트는 FastMCP 기반의 도구 서버와 LangChain-MCP 어댑터를 사용하여 LangGraph React Agent를 실행하는 예제입니다.  
서버에서는 `add`, `subtract` 두 가지 계산 도구를 제공하며, 클라이언트(에이전트)는 등록된 도구만 호출하고, 미지원 기능 요청 시에는 오류가 아닌 안내 메시지를 반환합니다.

---

## 주요 기능

- add(a, b): 두 숫자의 합을 계산합니다.  
- subtract(a, b): 첫 번째 숫자에서 두 번째 숫자를 뺍니다.

## 요구사항

- Python 3.8 이상  
- OpenAI API 키 (환경 변수 설정):

  ```bash
  export OPENAI_API_KEY=your_api_key_here
  ```

## 설치 및 실행 (자동 스크립트)

1. 권한 부여:

   ```bash
   cd mcp_agent
   chmod +x run.sh
   ```

2. 스크립트 실행:

   ```bash
   ./run.sh
   ```

   - **1/3**: 가상환경(`venv`) 생성  
   - **2/3**: 가상환경 활성화  
   - **3/3**: `requirements.txt` 기반 의존성 설치  
   - **4/4**: `langchain-mcp-adapters` 설치 (의존성 무시) 및 클라이언트(에이전트) 자동 실행

실행 시 자동으로 서버가 내부 프로세스로 시작되며, 에이전트가 대화형 프롬프트를 띄웁니다.

## 수동 설치 및 실행

```bash
cd mcp_agent
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --no-deps git+https://github.com/langchain-ai/langchain-mcp-adapters@b703a330e30c299db2a231874f42e25a5aebf1dd
```

## 계산 예시

```
계산할 내용을 입력하세요 (예: 3 더하기 5): 10 곱하기 5
```  
- `add`, `subtract` 호출 시 정상 수행  
- 그 외(예: `multiply`, `divide`) 요청 시:
  > 죄송합니다. 해당 기능을 지원하지 않습니다.

## 프로젝트 구조

```
mcp_agent/
├── run.sh            # 설치 및 자동 실행 스크립트
├── requirements.txt  # 고정된 의존성 목록
├── mcp_server.py     # FastMCP 서버 (add, subtract 도구)
├── mcp_client.py     # LangGraph React Agent 클라이언트
└── README.md         # 프로젝트 설명
```

---
