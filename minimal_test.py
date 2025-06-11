#!/usr/bin/env python3
import sys
import json
import struct
import subprocess
import os

# 设置二进制模式
if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

def main():
    try:
        # 写入启动日志
        with open("minimal_test.log", "w") as log:
            log.write("Minimal test script started\n")
            log.flush()
        
        # 读取输入
        length_data = sys.stdin.buffer.read(4)
        if len(length_data) == 4:
            length = struct.unpack('<I', length_data)[0]
            message_data = sys.stdin.buffer.read(length)
            message = json.loads(message_data.decode('utf-8'))
            
            # 记录消息
            with open("minimal_test.log", "a") as log:
                log.write(f"Received message: {message}\n")
            
            # 启动Chrome
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(chrome_path):
                url = message.get("url", "https://www.google.com")
                subprocess.Popen([chrome_path, "--new-window", url])
                
                response = {"success": True, "message": "Chrome started"}
            else:
                response = {"success": False, "error": "Chrome not found"}
            
            # 发送响应
            response_json = json.dumps(response)
            response_bytes = response_json.encode('utf-8')
            length_bytes = struct.pack('<I', len(response_bytes))
            
            sys.stdout.buffer.write(length_bytes)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()
            
            with open("minimal_test.log", "a") as log:
                log.write(f"Sent response: {response}\n")
        
    except Exception as e:
        with open("minimal_test.log", "a") as log:
            log.write(f"Error: {e}\n")

if __name__ == "__main__":
    main()
