#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 智能路径管理器
自动检测和修复所有路径配置
"""

import os
import json
import winreg
import sys
import shutil
from pathlib import Path

class PathManager:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.project_root = self.script_dir.parent
        self.extension_id = "bekgmlladkakjohmhaekpmbiobcggpnb"
        
        print(f"🔍 检测到项目根目录: {self.project_root}")
        
    def detect_current_paths(self):
        """检测当前路径配置"""
        print("\n📋 当前路径配置检测:")
        print("=" * 50)
        
        paths_info = {
            "project_root": str(self.project_root),
            "script_dir": str(self.script_dir),
            "extension_dir": str(self.project_root / "extension"),
            "native_host_dir": str(self.script_dir),
            "logs_dir": str(self.project_root / "logs")
        }
        
        for name, path in paths_info.items():
            exists = os.path.exists(path)
            print(f"   {name}: {path} {'✅' if exists else '❌'}")
        
        return paths_info
    
    def check_required_files(self):
        """检查必需文件"""
        print("\n📄 必需文件检查:")
        print("=" * 50)
        
        required_files = {
            "固定版Python脚本": "edge2chrome_launcher_edge_fixed.py",
            "固定版批处理文件": "edge2chrome_launcher_edge_fixed.bat", 
            "配置文件": "com.edge2chrome.launcher.json",
            "扩展manifest": "extension/manifest.json",
            "扩展background": "extension/background.js",
            "扩展content": "extension/content.js"
        }
        
        all_exist = True
        
        for desc, filename in required_files.items():
            filepath = self.project_root / filename
            exists = filepath.exists()
            print(f"   {desc}: {filepath} {'✅' if exists else '❌'}")
            if not exists:
                all_exist = False
        
        return all_exist
    
    def update_python_script(self):
        """更新Python脚本中的路径"""
        print("\n🐍 更新Python脚本路径...")
        
        script_path = self.project_root / "edge2chrome_launcher_edge_fixed.py"
        
        if not script_path.exists():
            print(f"❌ Python脚本不存在: {script_path}")
            return False
        
        try:
            # 读取当前内容
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换路径
            old_patterns = [
                r'D:\work\Edge2Chrome',
                r'D:\\work\\Edge2Chrome',
                r'C:\edge2chrome',
                r'C:\\edge2chrome',
                r'C:\edge2chrome_logs',
                r'C:\\edge2chrome_logs'
            ]
            
            new_project_path = str(self.project_root).replace('\\', '\\\\')
            new_logs_path = str(self.project_root / "logs").replace('\\', '\\\\')
            
            for pattern in old_patterns:
                if 'logs' in pattern:
                    content = content.replace(pattern, new_logs_path)
                else:
                    content = content.replace(pattern, new_project_path)
            
            # 写回文件
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 更新Python脚本: {script_path}")
            return True
            
        except Exception as e:
            print(f"❌ 更新Python脚本失败: {e}")
            return False
    
    def update_batch_file(self):
        """更新批处理文件"""
        print("\n📝 更新批处理文件...")
        
        bat_path = self.project_root / "edge2chrome_launcher_edge_fixed.bat"
        
        try:
            bat_content = f'''@echo off
cd /d "{self.project_root}"
python "edge2chrome_launcher_edge_fixed.py"
'''
            
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            
            print(f"✅ 更新批处理文件: {bat_path}")
            return True
            
        except Exception as e:
            print(f"❌ 更新批处理文件失败: {e}")
            return False
    
    def update_config_file(self):
        """更新配置文件"""
        print("\n⚙️ 更新配置文件...")
        
        config_path = self.project_root / "com.edge2chrome.launcher.json"
        bat_path = self.project_root / "edge2chrome_launcher_edge_fixed.bat"
        
        try:
            config = {
                "name": "com.edge2chrome.launcher",
                "description": "Edge2Chrome Native Host Fixed",
                "path": str(bat_path),
                "type": "stdio",
                "allowed_origins": [
                    f"chrome-extension://{self.extension_id}/"
                ]
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 更新配置文件: {config_path}")
            print(f"📋 配置内容:")
            print(json.dumps(config, indent=2, ensure_ascii=False))
            
            return True
            
        except Exception as e:
            print(f"❌ 更新配置文件失败: {e}")
            return False
    
    def update_registry(self):
        """更新注册表"""
        print("\n📝 更新注册表...")
        
        config_path = self.project_root / "com.edge2chrome.launcher.json"
        
        if not config_path.exists():
            print(f"❌ 配置文件不存在: {config_path}")
            return False
        
        try:
            key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, str(config_path))
            
            print(f"✅ 更新注册表: HKEY_CURRENT_USER\\{key_path}")
            print(f"📋 指向配置文件: {config_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ 更新注册表失败: {e}")
            return False
    
    def verify_registry(self):
        """验证注册表配置"""
        print("\n🔍 验证注册表配置...")
        
        try:
            key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                registered_path = winreg.QueryValue(key, "")
                
                print(f"📋 注册表路径: {registered_path}")
                
                if os.path.exists(registered_path):
                    print("✅ 配置文件存在")
                    
                    # 检查配置文件内容
                    with open(registered_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    bat_path = config.get('path', '')
                    if os.path.exists(bat_path):
                        print("✅ 批处理文件存在")
                        return True
                    else:
                        print(f"❌ 批处理文件不存在: {bat_path}")
                        return False
                else:
                    print(f"❌ 配置文件不存在: {registered_path}")
                    return False
                    
        except Exception as e:
            print(f"❌ 注册表验证失败: {e}")
            return False
    
    def create_missing_files(self):
        """创建缺失文件"""
        print("\n🔧 创建缺失文件...")
        
        # 创建日志目录
        logs_dir = self.project_root / "logs"
        logs_dir.mkdir(exist_ok=True)
        print(f"✅ 确保日志目录存在: {logs_dir}")
        
        # 检查并创建Python脚本
        python_script = self.project_root / "edge2chrome_launcher_edge_fixed.py"
        if not python_script.exists():
            print(f"⚠️ Python脚本不存在: {python_script}")
            print("   请确保已创建该文件")
            return False
        
        return True
    
    def run_diagnostic(self):
        """运行完整诊断"""
        print("\n🔍 运行完整路径诊断...")
        
        # 基础检查
        paths_ok = self.detect_current_paths()
        files_ok = self.check_required_files()
        
        if not files_ok:
            print("\n❌ 存在缺失文件，请先创建必需文件")
            return False
        
        # 验证注册表
        registry_ok = self.verify_registry()
        
        print(f"\n📊 诊断结果:")
        print(f"   路径检测: ✅")
        print(f"   文件检查: {'✅' if files_ok else '❌'}")
        print(f"   注册表: {'✅' if registry_ok else '❌'}")
        
        return files_ok and registry_ok
    
    def fix_all_paths(self):
        """修复所有路径配置"""
        print("\n🔧 开始修复所有路径配置...")
        print("=" * 60)
        
        success_count = 0
        total_steps = 5
        
        # 1. 创建缺失文件/目录
        if self.create_missing_files():
            success_count += 1
        
        # 2. 更新Python脚本
        if self.update_python_script():
            success_count += 1
        
        # 3. 更新批处理文件
        if self.update_batch_file():
            success_count += 1
        
        # 4. 更新配置文件
        if self.update_config_file():
            success_count += 1
        
        # 5. 更新注册表
        if self.update_registry():
            success_count += 1
        
        print(f"\n📊 修复结果: {success_count}/{total_steps} 步骤成功")
        
        if success_count == total_steps:
            print("🎉 所有路径配置修复完成！")
            return True
        else:
            print("⚠️ 部分步骤失败，请查看上面的错误信息")
            return False

def main():
    print("🎯 Edge2Chrome 智能路径管理器")
    print("=" * 60)
    
    manager = PathManager()
    
    while True:
        print(f"\n当前项目路径: {manager.project_root}")
        print("\n请选择操作:")
        print("1. 检测当前路径配置")
        print("2. 运行完整诊断")
        print("3. 一键修复所有路径")
        print("4. 仅更新注册表")
        print("5. 验证配置")
        print("0. 退出")
        
        choice = input("\n请输入选项 (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            manager.detect_current_paths()
            manager.check_required_files()
        elif choice == '2':
            manager.run_diagnostic()
        elif choice == '3':
            if manager.fix_all_paths():
                print("\n🎉 修复完成！请重启Edge并测试扩展")
            else:
                print("\n❌ 修复失败，请检查错误信息")
        elif choice == '4':
            if manager.update_registry():
                print("\n✅ 注册表更新完成")
            else:
                print("\n❌ 注册表更新失败")
        elif choice == '5':
            if manager.verify_registry():
                print("\n✅ 配置验证通过")
            else:
                print("\n❌ 配置验证失败")
        else:
            print("❌ 无效选项")
        
        input("\n按Enter继续...")

if __name__ == "__main__":
    main()