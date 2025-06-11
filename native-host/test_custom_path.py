#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义路径测试工具
"""

import subprocess
import json
import struct
import sys
import os

PROJECT_PATH = r"D:\work\Edge2Chrome"

def test_native_messaging():
    """测试Native Messaging通信"""
    print("🧪 测试自定义路径的Native Messaging")
    print("=" * 50)
    
    script_path = os.path.join(PROJECT_PATH, "edge2chrome_launcher_edge.py")
    
    if not os.path.exists(script_path):
        print(f"❌ Python脚本不存在: {script_path}")
        return False
    
    try:
        # 启动Native Host
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=PROJECT_PATH  # 设置工作目录
        )
        
        # 准备消息
        test_message = {
            "url": "https://www.zhihu.com/test-custom-path",
            "source": "custom-path-test",
            "chromeArgs": "--new-window"
        }
        
        print(f"📤 发送消息: {test_message}")
        
        # 编码消息
        message_json = json.dumps(test_message)
        message_bytes = message_json.encode('utf-8')
        length_bytes = struct.pack('<I', len(message_bytes))
        
        # 发送消息
        process.stdin.write(length_bytes)
        process.stdin.write(message_bytes)
        process.stdin.flush()
        process.stdin.close()
        
        # 读取响应
        try:
            stdout, stderr = process.communicate(timeout=10)
            
            print(f"📥 程序输出: {len(stdout)} 字节")
            if stderr:
                print(f"📥 错误输出: {stderr.decode('utf-8')}")
            
            if len(stdout) >= 4:
                # 解析响应
                response_length = struct.unpack('<I', stdout[:4])[0]
                if len(stdout) >= 4 + response_length:
                    response_data = stdout[4:4+response_length]
                    response = json.loads(response_data.decode('utf-8'))
                    
                    print(f"📋 响应: {response}")
                    
                    if response.get('success'):
                        print("✅ 测试成功！")
                        return True
                    else:
                        print(f"❌ 测试失败: {response.get('error')}")
                        return False
            else:
                print("❌ 没有收到有效响应")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            print("⏰ 程序响应超时")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def check_log_file():
    """检查日志文件"""
    print("\n📋 检查日志文件...")
    
    log_path = os.path.join(PROJECT_PATH, "logs", "edge_native.log")
    
    if os.path.exists(log_path):
        print(f"✅ 日志文件存在: {log_path}")
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.strip():
                print(f"📋 日志内容 (最后500字符):")
                print("-" * 50)
                print(content[-500:])
                print("-" * 50)
            else:
                print("📋 日志文件为空")
                
        except Exception as e:
            print(f"❌ 读取日志失败: {e}")
    else:
        print(f"❌ 日志文件不存在: {log_path}")

def main():
    print("🎯 Edge2Chrome 自定义路径测试")
    print("=" * 60)
    print(f"项目路径: {PROJECT_PATH}")
    
    # 检查项目路径
    if not os.path.exists(PROJECT_PATH):
        print(f"❌ 项目路径不存在: {PROJECT_PATH}")
        input("按Enter退出...")
        return
    
    # 测试Native Messaging
    test_ok = test_native_messaging()
    
    # 检查日志
    check_log_file()
    
    print("\n" + "=" * 60)
    print("📊 测试结果:")
    print(f"   通信测试: {'✅' if test_ok else '❌'}")
    
    if test_ok:
        print("\n🎉 测试通过！可以在Edge中使用扩展了")
    else:
        print("\n❌ 测试失败，请检查配置")
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()