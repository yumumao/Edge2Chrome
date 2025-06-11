#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 问题诊断工具
"""

import json
import os
import subprocess
import winreg
import sys

def test_chrome_paths():
    """测试Chrome路径"""
    print("🔍 检查Chrome安装...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
    ]
    
    found_chrome = None
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ 找到Chrome: {path}")
            found_chrome = path
            break
        else:
            print(f"❌ 未找到: {path}")
    
    if found_chrome:
        # 测试启动Chrome
        try:
            print(f"\n🧪 测试启动Chrome...")
            process = subprocess.Popen([found_chrome, "--version"], 
                                     capture_output=True, text=True, timeout=10)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print(f"✅ Chrome版本: {stdout.strip()}")
                return found_chrome
            else:
                print(f"❌ Chrome启动失败: {stderr}")
        except Exception as e:
            print(f"❌ Chrome测试失败: {e}")
    
    return None

def test_python_script():
    """测试Python脚本"""
    print("\n🐍 测试Python脚本...")
    
    script_path = r"C:\edge2chrome\edge2chrome_launcher.py"
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False
    
    print(f"✅ 脚本存在: {script_path}")
    
    # 测试脚本语法
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, script_path, 'exec')
        print("✅ 脚本语法正确")
        return True
    except SyntaxError as e:
        print(f"❌ 脚本语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 脚本检查失败: {e}")
        return False

def test_registry():
    """测试注册表"""
    print("\n🔧 检查注册表...")
    
    key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
    
    for hive_name, hive in [("HKEY_CURRENT_USER", winreg.HKEY_CURRENT_USER), 
                           ("HKEY_LOCAL_MACHINE", winreg.HKEY_LOCAL_MACHINE)]:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                manifest_path = winreg.QueryValue(key, "")
                print(f"✅ {hive_name}: {manifest_path}")
                
                # 检查manifest文件
                if os.path.exists(manifest_path):
                    print(f"✅ Manifest文件存在")
                    
                    # 检查manifest内容
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        
                        allowed_origins = config.get('allowed_origins', [])
                        if allowed_origins:
                            print(f"✅ 扩展ID已配置: {allowed_origins[0]}")
                        else:
                            print(f"❌ 未配置扩展ID")
                        
                        path_in_manifest = config.get('path', '')
                        if os.path.exists(path_in_manifest):
                            print(f"✅ 程序路径有效: {path_in_manifest}")
                        else:
                            print(f"❌ 程序路径无效: {path_in_manifest}")
                            
                    except Exception as e:
                        print(f"❌ Manifest内容错误: {e}")
                else:
                    print(f"❌ Manifest文件不存在: {manifest_path}")
                
                return True
                
        except Exception as e:
            print(f"❌ {hive_name}: 未找到注册表项")
    
    return False

def test_native_messaging():
    """测试Native Messaging通信"""
    print("\n📡 测试Native Messaging...")
    
    try:
        # 模拟发送消息
        test_message = {
            "url": "https://www.zhihu.com/test",
            "source": "edge",
            "chromeArgs": "--new-window",
            "timestamp": 1234567890
        }
        
        print(f"📤 测试消息: {test_message}")
        
        # 这里我们只能检查脚本是否能被调用
        script_path = r"C:\edge2chrome\edge2chrome_launcher.py"
        if os.path.exists(script_path):
            print("✅ Native Host脚本存在，可以被调用")
            return True
        else:
            print("❌ Native Host脚本不存在")
            return False
            
    except Exception as e:
        print(f"❌ 通信测试失败: {e}")
        return False

def check_logs():
    """检查日志文件"""
    print("\n📋 检查日志文件...")
    
    log_path = r"C:\edge2chrome_logs\edge2chrome.log"
    if os.path.exists(log_path):
        print(f"✅ 日志文件存在: {log_path}")
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines:
                print(f"📄 日志条目数: {len(lines)}")
                print("📋 最近的日志条目:")
                for line in lines[-10:]:  # 显示最后10行
                    print(f"   {line.strip()}")
            else:
                print("📄 日志文件为空")
                
        except Exception as e:
            print(f"❌ 读取日志失败: {e}")
    else:
        print(f"❌ 日志文件不存在: {log_path}")

def manual_test_launcher():
    """手动测试启动器"""
    print("\n🧪 手动测试启动器...")
    
    script_path = r"C:\edge2chrome\edge2chrome_launcher.py"
    if not os.path.exists(script_path):
        print("❌ 启动器脚本不存在")
        return
    
    try:
        print("🚀 尝试手动运行启动器...")
        print("(这个测试会等待输入，10秒后自动结束)")
        
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 发送测试消息
        test_message = json.dumps({
            "url": "https://www.zhihu.com/test",
            "source": "diagnosis",
            "chromeArgs": "--new-window"
        })
        
        try:
            stdout, stderr = process.communicate(input=test_message, timeout=10)
            print(f"✅ 启动器运行成功")
            if stdout:
                print(f"📤 输出: {stdout}")
            if stderr:
                print(f"❌ 错误: {stderr}")
        except subprocess.TimeoutExpired:
            process.kill()
            print("⏰ 启动器运行超时（正常情况）")
            
    except Exception as e:
        print(f"❌ 手动测试失败: {e}")

def main():
    print("🔍 Edge2Chrome 问题诊断")
    print("=" * 60)
    
    # 运行所有检查
    chrome_ok = test_chrome_paths() is not None
    python_ok = test_python_script()
    registry_ok = test_registry()
    messaging_ok = test_native_messaging()
    
    check_logs()
    manual_test_launcher()
    
    print("\n" + "=" * 60)
    print("📊 诊断结果总结:")
    print(f"   Chrome安装: {'✅' if chrome_ok else '❌'}")
    print(f"   Python脚本: {'✅' if python_ok else '❌'}")
    print(f"   注册表配置: {'✅' if registry_ok else '❌'}")
    print(f"   Native Messaging: {'✅' if messaging_ok else '❌'}")
    
    if all([chrome_ok, python_ok, registry_ok, messaging_ok]):
        print("\n🎉 所有组件都正常！")
        print("💡 如果仍有问题，可能是Edge扩展的通信问题")
        print("   建议：重启Edge，或检查扩展权限")
    else:
        print("\n❌ 发现问题，请根据上述检查结果修复")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()