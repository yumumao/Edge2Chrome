#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用Edge Native Messaging终极修复
"""

import os
import json
import winreg
import shutil
from pathlib import Path

def apply_ultimate_fix():
    """应用终极修复"""
    print("🚀 Edge2Chrome 终极修复")
    print("=" * 60)
    
    # 检测项目路径
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print(f"项目路径: {project_root}")
    
    try:
        # 1. 创建终极版批处理文件
        bat_content = f'''@echo off
cd /d "{project_root}"
python "edge2chrome_launcher_edge_ultimate.py"
'''
        
        bat_path = project_root / "edge2chrome_launcher_edge_ultimate.bat"
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        print(f"✅ 创建终极版批处理: {bat_path}")
        
        # 2. 更新配置文件
        config = {
            "name": "com.edge2chrome.launcher",
            "description": "Edge2Chrome Native Host Ultimate",
            "path": str(bat_path),
            "type": "stdio",
            "allowed_origins": [
                "chrome-extension://bekgmlladkakjohmhaekpmbiobcggpnb/"
            ]
        }
        
        config_path = project_root / "com.edge2chrome.launcher.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 更新配置文件: {config_path}")
        
        # 3. 更新注册表
        key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, str(config_path))
        print(f"✅ 更新注册表: {key_path}")
        
        # 4. 备份旧的background.js
        background_path = project_root / "extension" / "background.js"
        if background_path.exists():
            backup_path = project_root / "extension" / "background.js.backup"
            shutil.copy2(background_path, backup_path)
            print(f"✅ 备份background.js: {backup_path}")
        
        print("\n🎉 终极修复应用完成！")
        print("\n📋 下一步操作:")
        print("1. 确保已创建 edge2chrome_launcher_edge_ultimate.py")
        print("2. 用新的background.js代码更新扩展")
        print("3. 重新加载Edge扩展")
        print("4. 完全重启Edge浏览器")
        print("5. 测试扩展功能")
        print(f"6. 查看日志: {project_root / 'logs' / 'edge_ultimate.log'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 终极修复失败: {e}")
        return False

def main():
    if apply_ultimate_fix():
        print("\n✅ 修复完成")
    else:
        print("\n❌ 修复失败")
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()