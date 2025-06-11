#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查扩展ID配置
"""

import json
import os

def check_extension_id():
    """检查扩展ID配置"""
    print("🔍 检查扩展ID配置")
    print("=" * 50)
    
    manifest_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    
    if not os.path.exists(manifest_path):
        print(f"❌ 配置文件不存在: {manifest_path}")
        return False
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"📋 配置文件内容:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        allowed_origins = config.get('allowed_origins', [])
        if not allowed_origins:
            print("❌ 没有配置 allowed_origins")
            return False
        
        origin = allowed_origins[0]
        print(f"\n🔗 配置的扩展来源: {origin}")
        
        if "你的扩展ID" in origin:
            print("❌ 扩展ID尚未配置（仍为默认值）")
            return False
        
        # 提取扩展ID
        if origin.startswith("chrome-extension://") and origin.endswith("/"):
            extension_id = origin[19:-1]  # 去掉前缀和后缀
            print(f"📋 扩展ID: {extension_id}")
            
            if len(extension_id) == 32:
                print("✅ 扩展ID格式正确")
                return True
            else:
                print(f"❌ 扩展ID长度错误: {len(extension_id)} (应为32)")
                return False
        else:
            print(f"❌ origin格式错误: {origin}")
            return False
            
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def get_current_extension_id():
    """获取当前Edge中的扩展ID"""
    print("\n📋 获取扩展ID的步骤:")
    print("1. 打开Edge浏览器")
    print("2. 访问: edge://extensions/")
    print("3. 找到Edge2Chrome扩展")
    print("4. 复制ID行中的32位字符")
    print("   例如: ID: abcdefghijklmnopqrstuvwxyzabcdef")
    print("5. 只复制: abcdefghijklmnopqrstuvwxyzabcdef")
    
    extension_id = input("\n请输入扩展ID: ").strip()
    return extension_id

def update_extension_id(extension_id):
    """更新扩展ID"""
    manifest_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config['allowed_origins'] = [f"chrome-extension://{extension_id}/"]
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 扩展ID更新成功: {extension_id}")
        return True
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return False

def main():
    print("🔧 Edge2Chrome 扩展ID检查工具")
    print("=" * 60)
    
    if check_extension_id():
        print("\n🎉 扩展ID配置正确！")
        
        print("\n🔄 如果扩展仍不工作，请:")
        print("1. 完全关闭Edge浏览器")
        print("2. 重新打开Edge")
        print("3. 测试扩展功能")
        
    else:
        print("\n❌ 扩展ID配置有问题")
        
        response = input("是否现在配置扩展ID? (y/N): ").lower()
        if response == 'y':
            extension_id = get_current_extension_id()
            
            if extension_id and len(extension_id) == 32:
                if update_extension_id(extension_id):
                    print("\n🎉 配置完成！请重启Edge浏览器测试")
                else:
                    print("\n❌ 配置失败")
            else:
                print("❌ 扩展ID格式不正确")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()