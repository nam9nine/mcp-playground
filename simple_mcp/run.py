#!/usr/bin/env python
import os
import sys
import subprocess
import time
import signal
import atexit

# 백그라운드로 실행된 서버 프로세스를 저장
server_process = None

def cleanup():
    """프로그램 종료 시 백그라운드 프로세스 정리"""
    global server_process
    if server_process:
        print("백그라운드 서버를 종료합니다...")
        if sys.platform == 'win32':
            # Windows에서는 SIGTERM이 없으므로 terminate() 사용
            server_process.terminate()
        else:
            # Unix 시스템에서는 SIGTERM 사용
            os.kill(server_process.pid, signal.SIGTERM)

# 종료 시 정리 함수 등록
atexit.register(cleanup)

def check_venv():
    """가상환경이 활성화되어 있는지 확인"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def setup_environment():
    """가상환경 설정 및 필요한 패키지 설치"""
    if not os.path.exists('venv'):
        print("가상환경을 생성합니다...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    # 가상환경 활성화 경로
    if sys.platform == 'win32':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        pip_path = os.path.join('venv', 'Scripts', 'pip')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        pip_path = os.path.join('venv', 'bin', 'pip')
    
    # 패키지 설치
    print("필요한 패키지를 설치합니다...")
    if sys.platform == 'win32':
        subprocess.run([pip_path, 'install', '-U', 'fastmcp'])
    else:
        subprocess.run(['source', activate_script, '&&', pip_path, 'install', '-U', 'fastmcp'], shell=True)

def show_menu():
    """메뉴 표시"""
    print("\n=== MCP 예제 실행 메뉴 ===")
    print("1. STDIO 모드 실행")
    print("2. SSE 모드 실행 (서버+클라이언트)")
    print("3. 종료")
    
    choice = input("\n선택: ")
    return choice

def run_example(choice):
    """선택한 예제 실행"""
    global server_process
    
    if choice == '1':
        # STDIO 모드: 클라이언트만 실행 (서버는 자동으로 실행됨)
        print("STDIO 클라이언트를 실행합니다...")
        subprocess.run([sys.executable, 'simple_stdio_client.py'])
    elif choice == '2':
        # SSE 모드: 서버를 백그라운드로 실행하고 클라이언트 실행
        print("SSE 서버를 백그라운드로 시작합니다...")
        server_process = subprocess.Popen([sys.executable, 'simple_seo_server.py'])
        
        # 서버가 시작될 때까지 잠시 대기
        time.sleep(1)
        
        print("SSE 클라이언트를 실행합니다...")
        client_process = subprocess.run([sys.executable, 'simple_seo_client.py'])
        
        # 클라이언트가 종료되면 서버도 종료
        if server_process:
            cleanup()
            server_process = None
            
    elif choice == '3':
        print("프로그램을 종료합니다.")
        sys.exit(0)
    else:
        print("잘못된 선택입니다. 다시 선택해주세요.")

def main():
    """메인 함수"""
    # simple_mcp 폴더 내부에 있으므로 디렉토리 변경 필요 없음
    
    if not check_venv():
        print("주의: 가상환경이 활성화되어 있지 않습니다.")
        setup_environment()
        print(f"다음 명령어로 가상환경을 활성화하세요:")
        if sys.platform == 'win32':
            print("venv\\Scripts\\activate")
        else:
            print("source venv/bin/activate")
        return
    
    while True:
        choice = show_menu()
        run_example(choice)

if __name__ == "__main__":
    main() 