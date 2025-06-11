#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Edge兼容性问题
"""

import os
import json
import shutil

def update_files():
    """更新所有文件"""
    print("🔧 修复Edge兼容性...")
    
    # 1. 复制Edge专用的Python脚本
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 这里假设你已经创建了edge2chrome_launcher_edge.py
    edge_script_content = '''# Edge专用脚本内容在上面'''
    
    try:
        # 创建Edge专用脚本（内容在上面提供）
        edge_script_path = r"C:\edge2chrome\edge2chrome_launcher_edge.py"
        print(f"✅ 请手动创建: {edge_script_path}")
        
        # 创建批处理文件
        bat_content = '''@echo off
cd /d "C:\\edge2chrome"
python "edge2chrome_launcher_edge.py"
'''
        bat_path = r"C:\edge2chrome\edge2chrome_launcher_edge.bat"
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        print(f"✅ 创建批处理文件: {bat_path}")
        
        # 更新配置文件
        config = {
            "name": "com.edge2chrome.launcher",
            "description": "Edge2Chrome Native Host for Edge",
            "path": "C:\\edge2chrome\\edge2chrome_launcher_edge.bat",
            "type": "stdio",
            "allowed_origins": [
                "chrome-extension://bekgmlladkakjohmhaekpmbiobcggpnb/"
            ]
        }
        
        config_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 更新配置文件: {config_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新文件失败: {e}")
        return False

def main():
    print("🔧 Edge2Chrome Edge兼容性修复")
    print("=" * 50)
    
    if update_files():
        print("\n🎉 修复完成！")
        print("\n📋 下一步操作:")
        print("1. 手动创建 edge2chrome_launcher_edge.py (使用上面提供的代码)")
        print("2. 重新加载Edge扩展")
        print("3. 重启Edge浏览器")
        print("4. 测试扩展功能")
    else:
        print("\n❌ 修复失败")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()