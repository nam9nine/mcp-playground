#!/usr/bin/env bash

# 빠른 설치 스크립트
# 실행 방법: ./install.sh

set -e

echo "[1/3] 가상환경 생성..."
python3 -m venv venv

echo "[2/3] 가상환경 활성화..."
# shellcheck source=/dev/null
source venv/bin/activate

echo "[3/3] 패키지 설치 (requirements.txt)..."
pip install --upgrade pip
pip install -r requirements.txt

# langchain-mcp-adapters 설치 (의존성 무시)
echo "[4/4] langchain-mcp-adapters 설치 (의존성 무시)..."
pip install --no-deps git+https://github.com/langchain-ai/langchain-mcp-adapters@b703a330e30c299db2a231874f42e25a5aebf1dd

echo "설치 완료!\n가상환경 활성화: source venv/bin/activate"

# 클라이언트 실행 (생성된 venv 환경에서 서버 자동 시작 및 Agent 실행)
echo "[4/4] 클라이언트 실행 (서버 자동 시작)..."
python mcp_client.py 