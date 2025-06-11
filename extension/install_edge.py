#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome Native Host 安装脚本
"""

import os
import sys
import winreg
import json
import shutil
import subprocess

def check_admin():
    """检查是否有管理员权限"""
    try:
        return os.getuid() == 0
    except AttributeError:
        # Windows系统
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

def install_native_host():
    """安装Native Host到系统"""
    
    print("🚀 Edge2Chrome Native Host 安装程序")
    print("=" * 50)
    
    # 获取当前脚本目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 目标安装目录
    install_dir = r"C:\edge2chrome"
    
    try:
        # 创建安装目录
        print(f"📁 创建安装目录: {install_dir}")
        os.makedirs(install_dir, exist_ok=True)
        
        # 复制Python脚本
        python_script = os.path.join(current_dir, "edge2chrome_launcher.py")
        target_script = os.path.join(install_dir, "edge2chrome_launcher.py")
        
        if os.path.exists(python_script):
            print("📋 复制Native Host程序...")
            shutil.copy2(python_script, target_script)
        else:
            print("❌ 错误: 找不到 edge2chrome_launcher.py")
            print(f"请确保 {python_script} 存在")
            return False
        
        # 创建批处理文件来启动Python脚本
        batch_file = os.path.join(install_dir, "edge2chrome_launcher.bat")
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(f'@echo off\npython "{target_script}"')
        
        # 创建Edge的manifest文件
        manifest = {
            "name": "com.edge2chrome.launcher",
            "description": "Edge2Chrome Native Host - 在Edge中用Chrome打开指定链接",
            "path": batch_file,
            "type": "stdio",
            "allowed_origins": [
                "chrome-extension://你的扩展ID/"
            ]
        }
        
        manifest_path = os.path.join(install_dir, "com.edge2chrome.launcher.json")
        print("📝 创建manifest文件...")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        # 为Edge注册到注册表
        print("🔧 注册到Edge注册表...")
        edge_registry_key = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
        
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, edge_registry_key) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, manifest_path)
            print("✅ Edge注册表项创建成功")
        except Exception as e:
            print(f"⚠️  Edge注册表写入失败: {e}")
            print("尝试写入到HKEY_LOCAL_MACHINE...")
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, edge_registry_key) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, manifest_path)
                print("✅ 系统级注册表项创建成功")
            except Exception as e2:
                print(f"❌ 系统级注册表写入也失败: {e2}")
                return False
        
        # 创建日志目录
        log_dir = r"C:\edge2chrome_logs"
        os.makedirs(log_dir, exist_ok=True)
        print(f"📋 创建日志目录: {log_dir}")
        
        print("\n✅ Native Host安装完成！")
        print(f"📁 安装目录: {install_dir}")
        print(f"📝 Manifest文件: {manifest_path}")
        print(f"📋 日志目录: {log_dir}")
        
        print("\n" + "=" * 60)
        print("🔧 下一步操作:")
        print("1. 在Edge中打开: edge://extensions/")
        print("2. 启用'开发人员模式'")
        print("3. 点击'加载解压缩的扩展'")
        print("4. 选择 extension 文件夹")
        print("5. 复制扩展ID")
        print("6. 编辑以下文件，将'你的扩展ID'替换为实际ID:")
        print(f"   {manifest_path}")
        print("7. 重启Edge浏览器")
        print("8. 访问包含知乎链接的页面进行测试")
        
        print("\n🔍 故障排除:")
        print(f"- 查看日志文件: {log_dir}\\edge2chrome.log")
        print("- 确保Python已安装并可在命令行中使用")
        print("- 确保Chrome浏览器已安装")
        
        return True
        
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        print("请尝试以管理员身份运行此脚本")
        return False

def test_python():
    """测试Python环境"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"🐍 Python版本: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python环境测试失败: {e}")
        return False

def main():
    print("Edge2Chrome Native Host 安装程序")
    print("版本: 1.0.0")
    print("=" * 60)
    
    # 检查Python环境
    if not test_python():
        print("请确保Python已正确安装")
        input("按Enter键退出...")
        return
    
    # 检查管理员权限
    if not check_admin():
        print("⚠️  建议以管理员身份运行此脚本以确保注册表写入成功")
        response = input("是否继续? (y/N): ").lower()
        if response != 'y':
            return
    
    # 执行安装
    if install_native_host():
        print("\n🎉 安装成功完成！")
    else:
        print("\n😞 安装失败，请查看错误信息")
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()