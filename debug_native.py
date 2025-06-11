#!/usr/bin/env python3
import sys
import os
import time

# 记录启动
start_time = time.strftime("%Y-%m-%d %H:%M:%S")
debug_log = r"D:\work\Edge2Chrome\debug_native.log"

try:
    with open(debug_log, "w", encoding="utf-8") as log:
        log.write(f"DEBUG: Native Host started at {start_time}\n")
        log.write(f"DEBUG: Python version: {sys.version}\n")
        log.write(f"DEBUG: Working directory: {os.getcwd()}\n")
        log.write(f"DEBUG: Arguments: {sys.argv}\n")
        log.flush()
    
    # 尝试读取stdin
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write("DEBUG: Attempting to read from stdin...\n")
        log.flush()
    
    # 设置二进制模式
    if sys.platform == "win32":
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    
    # 读取输入
    input_data = sys.stdin.buffer.read(4)
    
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write(f"DEBUG: Read {len(input_data)} bytes from stdin\n")
        if input_data:
            log.write(f"DEBUG: Input data: {input_data}\n")
        log.flush()
    
    # 如果有输入，尝试读取完整消息
    if len(input_data) == 4:
        import struct
        length = struct.unpack('<I', input_data)[0]
        
        with open(debug_log, "a", encoding="utf-8") as log:
            log.write(f"DEBUG: Message length: {length}\n")
            log.flush()
        
        if 0 < length < 1024:
            message_data = sys.stdin.buffer.read(length)
            
            with open(debug_log, "a", encoding="utf-8") as log:
                log.write(f"DEBUG: Message data: {message_data}\n")
                log.flush()
            
            # 发送简单响应
            import json
            response = {"success": True, "debug": True, "message": "Debug response"}
            response_json = json.dumps(response)
            response_bytes = response_json.encode('utf-8')
            response_length = struct.pack('<I', len(response_bytes))
            
            sys.stdout.buffer.write(response_length)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()
            
            with open(debug_log, "a", encoding="utf-8") as log:
                log.write(f"DEBUG: Sent response: {response_json}\n")
                log.flush()
    
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write("DEBUG: Script completed normally\n")
        log.flush()

except Exception as e:
    try:
        with open(debug_log, "a", encoding="utf-8") as log:
            log.write(f"DEBUG: Exception occurred: {e}\n")
            import traceback
            log.write(f"DEBUG: Traceback: {traceback.format_exc()}\n")
            log.flush()
    except:
        pass
