#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键修复扩展ID配置
"""

import json
import os
import re

def get_extension_id_from_user():
    """获取扩展ID"""
    print("📋 请按以下步骤获取扩展ID:")
    print("1. 打开Edge浏览器")
    print("2. 访问: edge://extensions/")
    print("3. 找到Edge2Chrome扩展")
    print("4. 复制ID (32位字符)")
    print("   格式类似: abcdefghijklmnopqrstuvwxyzabcdef")
    
    while True:
        extension_id = input("\n请输入扩展ID: ").strip()
        
        if not extension_id:
            print("❌ 扩展ID不能为空")
            continue
        
        # 验证格式
        if len(extension_id) == 32 and re.match(r'^[a-z]+$', extension_id):
            return extension_id
        else:
            print("❌ 扩展ID格式不正确")
            print("   应为32位小写字母")
            print("   例如: abcdefghijklmnopqrstuvwxyzabcdef")
            
            retry = input("是否重新输入? (y/N): ").lower()
            if retry != 'y':
                return None

def update_manifest_config(extension_id):
    """更新manifest配置"""
    manifest_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    
    try:
        # 读取现有配置
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 更新扩展ID
        config['allowed_origins'] = [f"chrome-extension://{extension_id}/"]
        
        # 写回文件
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 配置文件已更新")
        print(f"📝 扩展来源: chrome-extension://{extension_id}/")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新配置失败: {e}")
        return False

def verify_config():
    """验证配置"""
    manifest_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"\n📋 当前配置:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        allowed_origins = config.get('allowed_origins', [])
        if allowed_origins and 'chrome-extension://' in allowed_origins[0]:
            extension_id = allowed_origins[0].replace('chrome-extension://', '').replace('/', '')
            print(f"\n✅ 配置的扩展ID: {extension_id}")
            return True
        else:
            print(f"\n❌ 配置无效")
            return False
            
    except Exception as e:
        print(f"❌ 验证配置失败: {e}")
        return False

def main():
    print("🔧 扩展ID一键修复工具")
    print("=" * 50)
    
    # 检查现有配置
    print("📋 检查当前配置...")
    if verify_config():
        response = input("\n配置看起来正确，是否仍要重新配置? (y/N): ").lower()
        if response != 'y':
            print("配置保持不变")
            input("按Enter键退出...")
            return
    
    # 获取新的扩展ID
    extension_id = get_extension_id_from_user()
    
    if not extension_id:
        print("操作取消")
        input("按Enter键退出...")
        return
    
    # 更新配置
    if update_manifest_config(extension_id):
        print("\n🎉 配置更新成功!")
        print("\n📋 下一步:")
        print("1. 完全关闭Edge浏览器")
        print("2. 重新打开Edge")
        print("3. 测试扩展功能")
        
        # 再次验证
        print("\n🔄 验证更新后的配置...")
        verify_config()
    else:
        print("\n❌ 配置更新失败")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()