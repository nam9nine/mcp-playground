# 간단한 MCP 서버/클라이언트 예제

이 프로젝트는 FastMCP 라이브러리를 사용하여 간단한 MCP(Message Communication Protocol) 서버와 클라이언트를 구현한 예제입니다.

## 간편 실행 방법 (추천)

프로젝트를 쉽게 실행하기 위한 스크립트가 준비되어 있습니다:

### 윈도우에서 실행:
```bash
# simple_mcp 폴더 안에서
run.bat
```

### 맥/리눅스에서 실행:
```bash
# simple_mcp 폴더 안에서
./run.sh
```

이 스크립트는 자동으로 다음 작업을 수행합니다:
1. 가상환경 생성 (필요한 경우)
2. 가상환경 활성화
3. 최신 버전의 FastMCP 패키지 설치
4. 메뉴를 표시하여 원하는 예제를 선택할 수 있도록 함

### 실행 메뉴 옵션:
1. **STDIO 모드 실행** - 클라이언트를 실행하고 서버는 자동으로 서브프로세스로 실행됨
2. **SSE 모드 실행 (서버+클라이언트)** - SSE 서버를 백그라운드로 실행하고 클라이언트를 자동으로 실행
3. **종료** - 프로그램 종료

> **참고**: 
> - STDIO 모드에서는 클라이언트가 자동으로 서버를 서브프로세스로 실행합니다.
> - SSE 모드에서는 서버와 클라이언트가 자동으로 함께 실행됩니다. 클라이언트를 종료하면 서버도 자동으로 종료됩니다.

## 수동 설치 및 실행 방법

### 설치 방법

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

2. 필요한 라이브러리 설치:
```bash
pip install fastmcp
```

### 수동 실행 방법

#### STDIO 모드:
STDIO 모드에서는 클라이언트만 실행하면 됩니다. 클라이언트가 서버를 자동으로 실행합니다.

```bash
python simple_stdio_client.py
```

#### SSE 모드:
이 모드에서는 서버를 먼저 실행한 후 클라이언트를 실행해야 합니다.

1. 서버 실행:
```bash
python simple_seo_server.py
```

2. 새 터미널에서 클라이언트 실행:
```bash
python simple_seo_client.py
```

## 구현된 기능

### 서버
서버는 FastMCP를 사용하여 다음 기능을 툴로 제공합니다:
- `add(a: int, b: int) -> int`: 두 숫자를 더한 결과를 반환합니다.

### 클라이언트
클라이언트는 서버에 연결하여 도구를 호출하는 예제를 포함하고 있습니다. 