#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义路径安装脚本
"""

import os
import json
import winreg
import shutil

# 自定义项目路径
PROJECT_PATH = r"D:\work\Edge2Chrome"
EXTENSION_ID = "bekgmlladkakjohmhaekpmbiobcggpnb"

def create_directories():
    """创建必要目录"""
    try:
        os.makedirs(os.path.join(PROJECT_PATH, "logs"), exist_ok=True)
        print(f"✅ 创建目录: {PROJECT_PATH}")
        return True
    except Exception as e:
        print(f"❌ 创建目录失败: {e}")
        return False

def create_config_file():
    """创建配置文件"""
    try:
        config = {
            "name": "com.edge2chrome.launcher",
            "description": "Edge2Chrome Native Host for Edge",
            "path": os.path.join(PROJECT_PATH, "edge2chrome_launcher_edge.bat"),
            "type": "stdio",
            "allowed_origins": [
                f"chrome-extension://{EXTENSION_ID}/"
            ]
        }
        
        config_path = os.path.join(PROJECT_PATH, "com.edge2chrome.launcher.json")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 创建配置文件: {config_path}")
        print(f"📋 配置内容:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        return config_path
        
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return None

def create_batch_file():
    """创建批处理文件"""
    try:
        bat_content = f'''@echo off
cd /d "{PROJECT_PATH}"
python "edge2chrome_launcher_edge.py"
'''
        
        bat_path = os.path.join(PROJECT_PATH, "edge2chrome_launcher_edge.bat")
        
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        
        print(f"✅ 创建批处理文件: {bat_path}")
        return bat_path
        
    except Exception as e:
        print(f"❌ 创建批处理文件失败: {e}")
        return None

def register_native_host(config_path):
    """注册Native Host"""
    try:
        key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
        
        # 注册到当前用户
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, config_path)
        
        print(f"✅ 注册到注册表: HKEY_CURRENT_USER\\{key_path}")
        return True
        
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        return False

def verify_installation():
    """验证安装"""
    print("\n🔍 验证安装...")
    
    # 检查文件
    files_to_check = [
        "com.edge2chrome.launcher.json",
        "edge2chrome_launcher_edge.bat",
        "edge2chrome_launcher_edge.py"
    ]
    
    all_ok = True
    
    for filename in files_to_check:
        filepath = os.path.join(PROJECT_PATH, filename)
        if os.path.exists(filepath):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} 不存在")
            all_ok = False
    
    # 检查注册表
    try:
        key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            registered_path = winreg.QueryValue(key, "")
            print(f"✅ 注册表配置: {registered_path}")
    except:
        print("❌ 注册表配置不存在")
        all_ok = False
    
    return all_ok

def main():
    print("🔧 Edge2Chrome 自定义路径安装")
    print("=" * 50)
    print(f"项目路径: {PROJECT_PATH}")
    print(f"扩展ID: {EXTENSION_ID}")
    print("=" * 50)
    
    # 检查项目路径
    if not os.path.exists(PROJECT_PATH):
        print(f"❌ 项目路径不存在: {PROJECT_PATH}")
        input("按Enter退出...")
        return
    
    # 执行安装步骤
    success = True
    
    success &= create_directories()
    
    config_path = create_config_file()
    success &= config_path is not None
    
    success &= create_batch_file() is not None
    
    if config_path:
        success &= register_native_host(config_path)
    
    # 验证安装
    if success:
        print("\n🎉 安装完成！")
        
        if verify_installation():
            print("\n✅ 验证通过")
            print("\n📋 下一步:")
            print("1. 确保 edge2chrome_launcher_edge.py 文件存在且内容正确")
            print("2. 重新加载Edge扩展")
            print("3. 重启Edge浏览器")
            print("4. 测试扩展功能")
            print(f"5. 查看日志: {os.path.join(PROJECT_PATH, 'logs', 'edge_native.log')}")
        else:
            print("\n❌ 验证失败")
    else:
        print("\n❌ 安装失败")
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()