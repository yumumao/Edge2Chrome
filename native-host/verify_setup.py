#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 安装验证工具
"""

import json
import os
import subprocess
import winreg

def check_files():
    """检查文件是否存在"""
    files = [
        r"C:\edge2chrome\edge2chrome_launcher.py",
        r"C:\edge2chrome\edge2chrome_launcher.bat", 
        r"C:\edge2chrome\com.edge2chrome.launcher.json"
    ]
    
    print("📁 检查文件...")
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            return False
    return True

def check_registry():
    """检查注册表项"""
    print("\n🔧 检查注册表...")
    
    key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            manifest_path = winreg.QueryValue(key, "")
            print(f"✅ 用户注册表: {manifest_path}")
            return True
    except:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                manifest_path = winreg.QueryValue(key, "")
                print(f"✅ 系统注册表: {manifest_path}")
                return True
        except:
            print("❌ 注册表项未找到")
            return False

def check_manifest():
    """检查manifest配置"""
    print("\n📋 检查配置文件...")
    
    manifest_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        allowed_origins = config.get('allowed_origins', [])
        if allowed_origins and '你的扩展ID' not in allowed_origins[0]:
            print(f"✅ 扩展ID已配置: {allowed_origins[0]}")
            return True
        else:
            print("❌ 扩展ID未配置或仍为默认值")
            return False
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def check_python():
    """检查Python环境"""
    print("\n🐍 检查Python环境...")
    try:
        result = subprocess.run(['python', '--version'], 
                              capture_output=True, text=True)
        print(f"✅ {result.stdout.strip()}")
        return True
    except:
        print("❌ Python未安装或不在PATH中")
        return False

def main():
    print("🔍 Edge2Chrome 安装验证")
    print("=" * 50)
    
    checks = [
        check_python(),
        check_files(),
        check_registry(),
        check_manifest()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 所有检查通过！安装配置正确")
        print("\n📋 如果扩展仍不工作，请:")
        print("1. 重启Edge浏览器")
        print("2. 检查扩展是否已启用") 
        print("3. 查看日志: C:\\edge2chrome_logs\\edge2chrome.log")
    else:
        print("❌ 存在配置问题，请检查上述失败项")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()