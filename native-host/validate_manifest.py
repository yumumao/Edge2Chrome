#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 manifest.json 格式
"""

import json
import os

def validate_manifest():
    """验证manifest.json文件"""
    
    # 查找manifest文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(current_dir, "..", "extension", "manifest.json")
    manifest_path = os.path.normpath(manifest_path)
    
    print("🔍 验证 manifest.json 文件")
    print("=" * 50)
    print(f"📁 文件路径: {manifest_path}")
    
    # 检查文件是否存在
    if not os.path.exists(manifest_path):
        print("❌ manifest.json 文件不存在")
        return False
    
    try:
        # 读取并解析JSON
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"📄 文件大小: {len(content)} 字符")
        
        # 解析JSON
        manifest = json.loads(content)
        
        print("✅ JSON 格式正确")
        
        # 检查必要字段
        required_fields = [
            "manifest_version",
            "name", 
            "version",
            "description"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"⚠️  缺少必要字段: {', '.join(missing_fields)}")
        else:
            print("✅ 包含所有必要字段")
        
        # 显示基本信息
        print(f"\n📋 扩展信息:")
        print(f"   名称: {manifest.get('name', 'N/A')}")
        print(f"   版本: {manifest.get('version', 'N/A')}")
        print(f"   描述: {manifest.get('description', 'N/A')}")
        print(f"   Manifest版本: {manifest.get('manifest_version', 'N/A')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误:")
        print(f"   错误位置: 第 {e.lineno} 行, 第 {e.colno} 列")
        print(f"   错误信息: {e.msg}")
        
        # 显示错误位置的上下文
        lines = content.split('\n')
        if e.lineno <= len(lines):
            print(f"\n📍 错误上下文:")
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 2)
            
            for i in range(start, end):
                line_num = i + 1
                line = lines[i]
                if line_num == e.lineno:
                    print(f">>> {line_num:3d}: {line}")
                    print(f"    {' ' * (e.colno + 3)}^ 错误位置")
                else:
                    print(f"    {line_num:3d}: {line}")
        
        return False
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def create_correct_manifest():
    """创建正确的manifest.json文件"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(current_dir, "..", "extension", "manifest.json")
    manifest_path = os.path.normpath(manifest_path)
    
    correct_manifest = {
        "manifest_version": 3,
        "name": "Edge2Chrome",
        "version": "1.0.0",
        "description": "在Edge中检测指定链接，点击按钮用Chrome打开",
        "permissions": [
            "nativeMessaging",
            "activeTab",
            "storage"
        ],
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["content.js"],
                "css": ["style.css"]
            }
        ],
        "background": {
            "service_worker": "background.js"
        },
        "host_permissions": [
            "<all_urls>"
        ],
        "options_page": "options.html",
        "action": {
            "default_popup": "popup.html",
            "default_title": "Edge2Chrome设置"
        }
    }
    
    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(correct_manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已创建正确的 manifest.json 文件: {manifest_path}")
        return True
        
    except Exception as e:
        print(f"❌ 创建文件失败: {e}")
        return False

def main():
    print("🔧 Edge2Chrome Manifest 验证工具")
    print("=" * 60)
    
    # 验证现有文件
    if not validate_manifest():
        print("\n" + "=" * 60)
        response = input("是否自动修复 manifest.json? (y/N): ").lower()
        
        if response == 'y':
            if create_correct_manifest():
                print("\n🔄 重新验证修复后的文件...")
                validate_manifest()
        else:
            print("\n📋 请手动修复 manifest.json 文件")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()