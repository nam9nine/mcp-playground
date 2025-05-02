@echo off
echo MCP 예제 실행기

if not exist venv (
    echo 가상환경을 생성합니다...
    python -m venv venv
)

echo 가상환경을 활성화합니다...
call venv\Scripts\activate

echo 필요한 패키지를 설치합니다...
pip install -U fastmcp

echo 프로그램을 실행합니다...
python run.py

pause 