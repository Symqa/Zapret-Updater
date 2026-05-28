import psutil
import subprocess

def stop_zapret():
    # 1 остановка процесса запрета (если есть)
    for proc in psutil.process_iter(['pid', 'name']):
        if 'winws' in proc.info['name']:
            pid = proc.info["pid"]
    
            try:
                process = psutil.Process(pid)
                process.terminate()
                print(f"\nCurrent zapret-discord process has stopped..")
            except psutil.NoSuchProcess:
                pass
    
    # 2 остановка процесса WinDivert64.sys
    res = subprocess.run(['sc', 'stop', 'windivert'], capture_output=True, text=True, encoding='cp866')
    print("Windivert process has stopped..")
