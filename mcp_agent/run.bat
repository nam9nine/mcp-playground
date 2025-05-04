@echo off
REM 빠른 설치 및 실행 스크립트 (Windows)
REM 실행 방법: run.bat

REM 1) 가상환경 생성
if not exist venv (
    echo [1/5] 가상환경을 생성합니다...
    python -m venv venv
) else (
    echo [1/5] 이미 가상환경이 존재합니다.
)

REM 2) 가상환경 활성화
echo [2/5] 가상환경을 활성화합니다...
call venv\Scripts\activate

REM 3) 패키지 설치
echo [3/5] 패키지를 설치합니다 (requirements.txt)...
echo n | pip install --upgrade pip
pip install -r requirements.txt

REM 4) langchain-mcp-adapters 설치 (의존성 무시)
echo [4/5] langchain-mcp-adapters 설치 (의존성 무시)...
pip install --no-deps git+https://github.com/langchain-ai/langchain-mcp-adapters@b703a330e30c299db2a231874f42e25a5aebf1dd

REM 5) 클라이언트 실행 (서버 자동 시작)
echo [5/5] 클라이언트를 실행합니다 (서버 자동 시작)...
python mcp_client.py

pause 