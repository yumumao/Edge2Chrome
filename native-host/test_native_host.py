#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Native Host程序
"""

import subprocess
import json
import struct
import sys
import time

def test_native_host():
    """测试Native Host程序"""
    print("🧪 测试Native Host程序")
    print("=" * 50)
    
    script_path = r"C:\edge2chrome\edge2chrome_launcher.py"
    
    try:
        # 启动Native Host进程
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 准备测试消息
        test_message = {
            "url": "https://www.zhihu.com/question/12345",
            "source": "test",
            "chromeArgs": "--new-window"
        }
        
        print(f"📤 发送测试消息: {test_message}")
        
        # 将消息转换为Native Messaging格式
        message_json = json.dumps(test_message)
        message_bytes = message_json.encode('utf-8')
        length_bytes = struct.pack('<I', len(message_bytes))
        
        # 发送消息
        process.stdin.write(length_bytes)
        process.stdin.write(message_bytes)
        process.stdin.flush()
        
        # 读取响应
        print("📥 等待响应...")
        
        # 设置超时
        try:
            stdout, stderr = process.communicate(timeout=10)
            
            if stderr:
                print(f"❌ 错误输出: {stderr.decode('utf-8')}")
            
            if stdout:
                print(f"✅ 程序输出: {stdout.decode('utf-8')}")
                
                # 尝试解析响应
                if len(stdout) >= 4:
                    response_length = struct.unpack('<I', stdout[:4])[0]
                    if len(stdout) >= 4 + response_length:
                        response_data = stdout[4:4+response_length]
                        response = json.loads(response_data.decode('utf-8'))
                        print(f"📋 解析响应: {response}")
                        
                        if response.get('success'):
                            print("🎉 测试成功!")
                        else:
                            print(f"❌ 测试失败: {response.get('error')}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            print("⏰ 程序响应超时")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_chrome_direct():
    """直接测试Chrome启动"""
    print("\n🌐 直接测试Chrome启动")
    print("=" * 50)
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    test_url = "https://www.zhihu.com/question/12345"
    
    try:
        cmd = [chrome_path, "--new-window", test_url]
        print(f"🚀 执行命令: {' '.join(cmd)}")
        
        process = subprocess.Popen(cmd)
        print(f"✅ Chrome启动成功, PID: {process.pid}")
        
    except Exception as e:
        print(f"❌ Chrome启动失败: {e}")

if __name__ == "__main__":
    test_native_host()
    test_chrome_direct()
    input("\n按Enter键退出...")