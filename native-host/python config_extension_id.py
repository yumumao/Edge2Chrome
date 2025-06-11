#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 扩展ID配置工具
"""

import json
import os
import re

def find_manifest_file():
    """查找manifest文件"""
    possible_paths = [
        r"C:\edge2chrome\com.edge2chrome.launcher.json",
        r"C:\edge2chrome_launcher\com.edge2chrome.launcher.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def validate_extension_id(extension_id):
    """验证扩展ID格式"""
    # Edge扩展ID通常是32位小写字母
    pattern = r'^[a-z]{32}$'
    return bool(re.match(pattern, extension_id))

def update_manifest(manifest_path, extension_id):
    """更新manifest文件中的扩展ID"""
    try:
        # 读取现有配置
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 更新扩展ID
        config['allowed_origins'] = [f"chrome-extension://{extension_id}/"]
        
        # 写回文件
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"更新配置文件失败: {e}")
        return False

def main():
    print("🔧 Edge2Chrome 扩展ID配置工具")
    print("=" * 50)
    
    # 查找manifest文件
    manifest_path = find_manifest_file()
    if not manifest_path:
        print("❌ 找不到配置文件")
        print("请确保已正确安装Native Host")
        input("按Enter键退出...")
        return
    
    print(f"📝 找到配置文件: {manifest_path}")
    
    # 获取扩展ID
    while True:
        print("\n📋 请按以下步骤获取扩展ID:")
        print("1. 打开Edge浏览器")
        print("2. 访问 edge://extensions/")
        print("3. 找到Edge2Chrome扩展")
        print("4. 复制扩展ID（32位字母数字）")
        
        extension_id = input("\n请输入扩展ID: ").strip()
        
        if not extension_id:
            print("❌ 扩展ID不能为空")
            continue
        
        if not validate_extension_id(extension_id):
            print("❌ 扩展ID格式不正确")
            print("扩展ID应该是32位小写字母，例如: abcdefghijklmnopqrstuvwxyzabcdef")
            retry = input("是否重新输入? (y/N): ").lower()
            if retry != 'y':
                break
            continue
        
        break
    
    if not extension_id or not validate_extension_id(extension_id):
        print("配置取消")
        input("按Enter键退出...")
        return
    
    # 更新配置文件
    print(f"\n🔄 更新配置文件...")
    if update_manifest(manifest_path, extension_id):
        print("✅ 配置更新成功!")
        print(f"\n📋 已配置扩展ID: {extension_id}")
        print("\n🚀 下一步:")
        print("1. 完全关闭Edge浏览器")
        print("2. 重新打开Edge")
        print("3. 访问包含知乎链接的页面测试")
    else:
        print("❌ 配置更新失败")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()