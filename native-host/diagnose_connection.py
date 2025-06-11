#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断Native Host连接问题
"""

import json
import os
import winreg
import subprocess
import sys

def check_registry_detailed():
    """详细检查注册表"""
    print("🔧 详细检查注册表配置...")
    
    key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
    
    for hive_name, hive in [
        ("HKEY_CURRENT_USER", winreg.HKEY_CURRENT_USER),
        ("HKEY_LOCAL_MACHINE", winreg.HKEY_LOCAL_MACHINE)
    ]:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                manifest_path = winreg.QueryValue(key, "")
                print(f"✅ {hive_name}: {manifest_path}")
                
                # 检查manifest文件
                if os.path.exists(manifest_path):
                    print(f"✅ Manifest文件存在")
                    
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    print(f"📋 Manifest内容:")
                    print(json.dumps(config, indent=2, ensure_ascii=False))
                    
                    # 检查路径
                    bat_path = config.get('path', '')
                    if os.path.exists(bat_path):
                        print(f"✅ 批处理文件存在: {bat_path}")
                        
                        # 检查批处理文件内容
                        with open(bat_path, 'r') as f:
                            bat_content = f.read()
                        print(f"📋 批处理文件内容:\n{bat_content}")
                        
                    else:
                        print(f"❌ 批处理文件不存在: {bat_path}")
                    
                    return True
                else:
                    print(f"❌ Manifest文件不存在: {manifest_path}")
                    
        except Exception as e:
            print(f"❌ {hive_name}: {e}")
    
    return False

def test_bat_file():
    """测试批处理文件"""
    print("\n🧪 测试批处理文件...")
    
    bat_path = r"C:\edge2chrome\edge2chrome_launcher_edge.bat"
    
    if not os.path.exists(bat_path):
        print(f"❌ 批处理文件不存在: {bat_path}")
        return False
    
    try:
        # 测试运行批处理文件
        print(f"🚀 测试运行: {bat_path}")
        
        process = subprocess.Popen(
            [bat_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        
        # 发送测试数据
        test_input = json.dumps({
            "url": "https://www.zhihu.com/test",
            "source": "diagnosis"
        })
        
        try:
            stdout, stderr = process.communicate(input=test_input, timeout=5)
            
            if process.returncode == 0:
                print("✅ 批处理文件运行成功")
                if stdout:
                    print(f"📤 输出: {stdout}")
            else:
                print(f"❌ 批处理文件运行失败: {process.returncode}")
                if stderr:
                    print(f"错误: {stderr}")
            
            return process.returncode == 0
            
        except subprocess.TimeoutExpired:
            process.kill()
            print("⏰ 批处理文件响应超时（可能正常）")
            return True
            
    except Exception as e:
        print(f"❌ 测试批处理文件失败: {e}")
        return False

def check_python_script():
    """检查Python脚本"""
    print("\n🐍 检查Python脚本...")
    
    script_path = r"C:\edge2chrome\edge2chrome_launcher_edge.py"
    
    if not os.path.exists(script_path):
        print(f"❌ Python脚本不存在: {script_path}")
        return False
    
    try:
        # 检查语法
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, script_path, 'exec')
        print("✅ Python脚本语法正确")
        
        # 检查文件大小
        size = len(content)
        print(f"📋 脚本大小: {size} 字符")
        
        if size < 1000:
            print("⚠️ 脚本文件可能不完整")
            return False
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Python脚本语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 检查Python脚本失败: {e}")
        return False

def create_minimal_test():
    """创建最小测试环境"""
    print("\n🔧 创建最小测试环境...")
    
    try:
        # 创建最小的Python脚本
        minimal_script = '''import sys
import json
import struct

print("Minimal test script started", file=sys.stderr)

try:
    # 读取长度
    length_data = sys.stdin.buffer.read(4)
    if len(length_data) == 4:
        length = struct.unpack('<I', length_data)[0]
        print(f"Message length: {length}", file=sys.stderr)
        
        # 读取消息
        message_data = sys.stdin.buffer.read(length)
        message = json.loads(message_data.decode('utf-8'))
        print(f"Received: {message}", file=sys.stderr)
        
        # 发送响应
        response = {"success": True, "message": "Test successful"}
        response_json = json.dumps(response)
        response_bytes = response_json.encode('utf-8')
        response_length = struct.pack('<I', len(response_bytes))
        
        sys.stdout.buffer.write(response_length)
        sys.stdout.buffer.write(response_bytes)
        sys.stdout.buffer.flush()
        
        print("Response sent", file=sys.stderr)
    else:
        print("No input received", file=sys.stderr)
        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
'''
        
        # 保存最小脚本
        minimal_path = r"C:\edge2chrome\minimal_test.py"
        with open(minimal_path, 'w', encoding='utf-8') as f:
            f.write(minimal_script)
        
        # 创建测试批处理文件
        minimal_bat = '''@echo off
cd /d "C:\\edge2chrome"
python "minimal_test.py" 2>> minimal_test.log
'''
        
        minimal_bat_path = r"C:\edge2chrome\minimal_test.bat"
        with open(minimal_bat_path, 'w') as f:
            f.write(minimal_bat)
        
        print(f"✅ 创建最小测试脚本: {minimal_path}")
        print(f"✅ 创建最小测试批处理: {minimal_bat_path}")
        
        # 创建临时配置
        temp_config = {
            "name": "com.edge2chrome.launcher",
            "description": "Edge2Chrome Test",
            "path": minimal_bat_path,
            "type": "stdio",
            "allowed_origins": [
                "chrome-extension://bekgmlladkakjohmhaekpmbiobcggpnb/"
            ]
        }
        
        temp_config_path = r"C:\edge2chrome\test_config.json"
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            json.dump(temp_config, f, indent=2)
        
        print(f"✅ 创建测试配置: {temp_config_path}")
        print("\n📋 使用测试配置:")
        print("1. 备份当前配置")
        print("2. 将test_config.json重命名为com.edge2chrome.launcher.json")
        print("3. 重启Edge测试")
        print("4. 查看 C:\\edge2chrome\\minimal_test.log")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建测试环境失败: {e}")
        return False

def main():
    print("🔍 Native Host连接问题诊断")
    print("=" * 60)
    
    registry_ok = check_registry_detailed()
    bat_ok = test_bat_file()
    python_ok = check_python_script()
    
    print("\n" + "=" * 60)
    print("📊 诊断结果:")
    print(f"   注册表配置: {'✅' if registry_ok else '❌'}")
    print(f"   批处理文件: {'✅' if bat_ok else '❌'}")
    print(f"   Python脚本: {'✅' if python_ok else '❌'}")
    
    if not all([registry_ok, bat_ok, python_ok]):
        print("\n❌ 发现问题，建议创建最小测试环境")
        
        response = input("是否创建最小测试环境? (y/N): ").lower()
        if response == 'y':
            create_minimal_test()
    else:
        print("\n✅ 所有组件看起来正常")
        print("问题可能在于Edge的Native Messaging实现")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()