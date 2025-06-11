#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用Edge通信修复
"""

import os
import json
import winreg

PROJECT_PATH = r"D:\work\Edge2Chrome"

def apply_fix():
    """应用修复"""
    print("🔧 应用Edge通信修复...")
    
    try:
        # 1. 创建修复版批处理文件
        bat_content = f'''@echo off
cd /d "{PROJECT_PATH}"
python "edge2chrome_launcher_edge_fixed.py"
'''
        
        bat_path = os.path.join(PROJECT_PATH, "edge2chrome_launcher_edge_fixed.bat")
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        print(f"✅ 创建修复版批处理: {bat_path}")
        
        # 2. 更新配置文件
        config = {
            "name": "com.edge2chrome.launcher",
            "description": "Edge2Chrome Native Host Fixed",
            "path": bat_path,
            "type": "stdio",
            "allowed_origins": [
                "chrome-extension://bekgmlladkakjohmhaekpmbiobcggpnb/"
            ]
        }
        
        config_path = os.path.join(PROJECT_PATH, "com.edge2chrome.launcher.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 更新配置文件: {config_path}")
        
        # 3. 更新注册表
        key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, config_path)
        print(f"✅ 更新注册表配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 应用修复失败: {e}")
        return False

def main():
    print("🔧 Edge2Chrome Edge通信修复")
    print("=" * 50)
    
    # 检查修复版Python脚本是否存在
    fixed_script = os.path.join(PROJECT_PATH, "edge2chrome_launcher_edge_fixed.py")
    
    if not os.path.exists(fixed_script):
        print(f"❌ 修复版脚本不存在: {fixed_script}")
        print("请先创建该文件，使用上面提供的代码")
        input("按Enter退出...")
        return
    
    if apply_fix():
        print("\n🎉 修复应用成功！")
        print("\n📋 下一步:")
        print("1. 重新加载Edge扩展")
        print("2. 重启Edge浏览器")
        print("3. 测试扩展功能")
        print("4. 查看修复版日志: D:\\work\\Edge2Chrome\\logs\\edge_fixed.log")
    else:
        print("\n❌ 修复应用失败")
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()