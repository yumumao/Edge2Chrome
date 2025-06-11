#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理旧版本文件
"""

import os

PROJECT_PATH = r"D:\work\Edge2Chrome"

def cleanup_files():
    """清理旧文件"""
    print("🧹 清理旧版本文件...")
    
    files_to_delete = [
        "edge2chrome_launcher_edge.bat",
        "edge2chrome_launcher_edge.py", 
        "edge2chrome_launcher.py"
    ]
    
    deleted_count = 0
    
    for filename in files_to_delete:
        filepath = os.path.join(PROJECT_PATH, filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"✅ 删除: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 删除失败 {filename}: {e}")
        else:
            print(f"ℹ️ 文件不存在: {filename}")
    
    return deleted_count

def show_current_files():
    """显示当前文件"""
    print(f"\n📋 {PROJECT_PATH} 目录当前文件:")
    
    try:
        files = [f for f in os.listdir(PROJECT_PATH) if os.path.isfile(os.path.join(PROJECT_PATH, f))]
        
        for filename in sorted(files):
            if filename.endswith(('.py', '.bat', '.json')):
                print(f"   📄 {filename}")
    except Exception as e:
        print(f"❌ 列举文件失败: {e}")

def main():
    print("🧹 Edge2Chrome 文件清理工具")
    print("=" * 50)
    
    print("将要删除以下旧版本文件:")
    print("- edge2chrome_launcher_edge.bat")
    print("- edge2chrome_launcher_edge.py")
    print("- edge2chrome_launcher.py")
    
    response = input("\n确定要删除这些文件吗? (y/N): ").lower()
    
    if response == 'y':
        deleted = cleanup_files()
        print(f"\n🎉 清理完成！删除了 {deleted} 个文件")
    else:
        print("\n取消清理")
    
    show_current_files()
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()