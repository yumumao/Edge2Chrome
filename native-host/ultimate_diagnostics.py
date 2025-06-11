#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 终极诊断和修复工具
彻底解决Native Host连接问题
"""

import os
import json
import winreg
import subprocess
import sys
import time
import struct
from pathlib import Path

class UltimateDiagnostics:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.project_root = self.script_dir.parent
        self.extension_id = "bekgmlladkakjohmhaekpmbiobcggpnb"
        
        print(f"🔍 项目路径: {self.project_root}")
        print(f"🔍 扩展ID: {self.extension_id}")
    
    def test_python_environment(self):
        """测试Python环境"""
        print("\n🐍 测试Python环境")
        print("=" * 50)
        
        try:
            print(f"✅ Python版本: {sys.version}")
            print(f"✅ Python可执行文件: {sys.executable}")
            
            # 测试必需模块
            modules = ['json', 'struct', 'subprocess', 'winreg']
            for module in modules:
                try:
                    __import__(module)
                    print(f"✅ 模块 {module}: 可用")
                except ImportError:
                    print(f"❌ 模块 {module}: 不可用")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Python环境测试失败: {e}")
            return False
    
    def check_registry_detailed(self):
        """详细检查注册表"""
        print("\n📝 详细检查注册表")
        print("=" * 50)
        
        key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
        
        # 检查所有可能的注册表位置
        registry_locations = [
            ("HKEY_CURRENT_USER", winreg.HKEY_CURRENT_USER),
            ("HKEY_LOCAL_MACHINE", winreg.HKEY_LOCAL_MACHINE)
        ]
        
        found_valid_config = False
        
        for location_name, hive in registry_locations:
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    manifest_path = winreg.QueryValue(key, "")
                    print(f"✅ {location_name}: {manifest_path}")
                    
                    # 检查配置文件
                    if os.path.exists(manifest_path):
                        print(f"✅ 配置文件存在")
                        
                        try:
                            with open(manifest_path, 'r', encoding='utf-8') as f:
                                config = json.load(f)
                            
                            print(f"📋 配置内容:")
                            for key, value in config.items():
                                print(f"   {key}: {value}")
                            
                            # 检查路径是否正确
                            bat_path = config.get('path', '')
                            if os.path.exists(bat_path):
                                print(f"✅ 批处理文件存在: {bat_path}")
                                found_valid_config = True
                            else:
                                print(f"❌ 批处理文件不存在: {bat_path}")
                                
                        except Exception as e:
                            print(f"❌ 配置文件读取失败: {e}")
                    else:
                        print(f"❌ 配置文件不存在: {manifest_path}")
                        
            except Exception as e:
                print(f"❌ {location_name}: {e}")
        
        return found_valid_config
    
    def test_batch_file_execution(self):
        """测试批处理文件执行"""
        print("\n📝 测试批处理文件执行")
        print("=" * 50)
        
        # 寻找批处理文件
        possible_bat_files = [
            "edge2chrome_launcher_edge_ultimate.bat",
            "edge2chrome_launcher_edge_fixed.bat",
            "edge2chrome_launcher_edge.bat"
        ]
        
        bat_file = None
        for filename in possible_bat_files:
            path = self.project_root / filename
            if path.exists():
                bat_file = path
                break
        
        if not bat_file:
            print("❌ 找不到批处理文件")
            return False
        
        print(f"🔍 测试批处理文件: {bat_file}")
        
        try:
            # 读取批处理文件内容
            with open(bat_file, 'r') as f:
                content = f.read()
            print(f"📋 批处理文件内容:")
            print(content)
            
            # 测试执行
            print("🚀 测试执行批处理文件...")
            
            # 准备测试输入
            test_message = {
                "url": "https://www.zhihu.com/diagnostic-test",
                "source": "diagnostic",
                "chromeArgs": "--new-window"
            }
            
            message_json = json.dumps(test_message)
            message_bytes = message_json.encode('utf-8')
            length_bytes = struct.pack('<I', len(message_bytes))
            input_data = length_bytes + message_bytes
            
            # 启动进程
            process = subprocess.Popen(
                str(bat_file),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                cwd=str(self.project_root)
            )
            
            # 发送测试数据
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=10)
                
                print(f"📤 返回码: {process.returncode}")
                
                if stderr:
                    stderr_text = stderr.decode('utf-8', errors='ignore')
                    print(f"📤 错误输出:")
                    print(stderr_text)
                
                if stdout and len(stdout) >= 4:
                    # 解析响应
                    response_length = struct.unpack('<I', stdout[:4])[0]
                    if len(stdout) >= 4 + response_length:
                        response_data = stdout[4:4+response_length]
                        try:
                            response = json.loads(response_data.decode('utf-8'))
                            print(f"✅ 收到响应: {response}")
                            return True
                        except:
                            print(f"❌ 响应解析失败")
                            print(f"原始响应: {stdout}")
                else:
                    print("❌ 没有收到有效响应")
                    if stdout:
                        print(f"原始输出: {stdout}")
                
                return process.returncode == 0
                
            except subprocess.TimeoutExpired:
                process.kill()
                print("⏰ 批处理文件执行超时")
                return False
                
        except Exception as e:
            print(f"❌ 批处理文件测试失败: {e}")
            return False
    
    def create_minimal_test_setup(self):
        """创建最小测试设置"""
        print("\n🔧 创建最小测试设置")
        print("=" * 50)
        
        try:
            # 创建最简单的测试脚本
            minimal_script = '''#!/usr/bin/env python3
import sys
import json
import struct
import subprocess
import os

# 设置二进制模式
if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

def main():
    try:
        # 写入启动日志
        with open("minimal_test.log", "w") as log:
            log.write("Minimal test script started\\n")
            log.flush()
        
        # 读取输入
        length_data = sys.stdin.buffer.read(4)
        if len(length_data) == 4:
            length = struct.unpack('<I', length_data)[0]
            message_data = sys.stdin.buffer.read(length)
            message = json.loads(message_data.decode('utf-8'))
            
            # 记录消息
            with open("minimal_test.log", "a") as log:
                log.write(f"Received message: {message}\\n")
            
            # 启动Chrome
            chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if os.path.exists(chrome_path):
                url = message.get("url", "https://www.google.com")
                subprocess.Popen([chrome_path, "--new-window", url])
                
                response = {"success": True, "message": "Chrome started"}
            else:
                response = {"success": False, "error": "Chrome not found"}
            
            # 发送响应
            response_json = json.dumps(response)
            response_bytes = response_json.encode('utf-8')
            length_bytes = struct.pack('<I', len(response_bytes))
            
            sys.stdout.buffer.write(length_bytes)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()
            
            with open("minimal_test.log", "a") as log:
                log.write(f"Sent response: {response}\\n")
        
    except Exception as e:
        with open("minimal_test.log", "a") as log:
            log.write(f"Error: {e}\\n")

if __name__ == "__main__":
    main()
'''
            
            # 保存最小脚本
            minimal_script_path = self.project_root / "minimal_test.py"
            with open(minimal_script_path, 'w') as f:
                f.write(minimal_script)
            print(f"✅ 创建最小测试脚本: {minimal_script_path}")
            
            # 创建最小批处理文件
            minimal_bat_content = f'''@echo off
cd /d "{self.project_root}"
python "minimal_test.py"
'''
            
            minimal_bat_path = self.project_root / "minimal_test.bat"
            with open(minimal_bat_path, 'w') as f:
                f.write(minimal_bat_content)
            print(f"✅ 创建最小批处理文件: {minimal_bat_path}")
            
            # 创建最小配置文件
            minimal_config = {
                "name": "com.edge2chrome.launcher",
                "description": "Edge2Chrome Minimal Test",
                "path": str(minimal_bat_path),
                "type": "stdio",
                "allowed_origins": [
                    f"chrome-extension://{self.extension_id}/"
                ]
            }
            
            minimal_config_path = self.project_root / "minimal_config.json"
            with open(minimal_config_path, 'w', encoding='utf-8') as f:
                json.dump(minimal_config, f, indent=2, ensure_ascii=False)
            print(f"✅ 创建最小配置文件: {minimal_config_path}")
            
            return minimal_config_path
            
        except Exception as e:
            print(f"❌ 创建最小测试设置失败: {e}")
            return None
    
    def apply_minimal_config(self, config_path):
        """应用最小配置"""
        print(f"\n🔧 应用最小配置: {config_path}")
        
        try:
            # 备份当前配置
            current_config = self.project_root / "com.edge2chrome.launcher.json"
            if current_config.exists():
                backup_config = self.project_root / "com.edge2chrome.launcher.json.backup"
                import shutil
                shutil.copy2(current_config, backup_config)
                print(f"✅ 备份当前配置: {backup_config}")
            
            # 复制最小配置
            import shutil
            shutil.copy2(config_path, current_config)
            print(f"✅ 应用最小配置")
            
            # 更新注册表
            key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, str(current_config))
            print(f"✅ 更新注册表")
            
            return True
            
        except Exception as e:
            print(f"❌ 应用最小配置失败: {e}")
            return False
    
    def test_edge_connection(self):
        """测试Edge连接"""
        print("\n🔗 测试Edge连接")
        print("=" * 50)
        
        print("📋 请按以下步骤测试:")
        print("1. 重新加载Edge扩展")
        print("2. 完全重启Edge浏览器")
        print("3. 在Edge中访问知乎页面")
        print("4. 点击Chrome按钮")
        print("5. 查看是否有错误信息")
        print(f"6. 检查日志文件: {self.project_root / 'minimal_test.log'}")
        
        input("完成测试后按Enter继续...")
        
        # 检查日志文件
        log_file = self.project_root / "minimal_test.log"
        if log_file.exists():
            print("📋 找到测试日志:")
            with open(log_file, 'r') as f:
                content = f.read()
            print(content)
            return True
        else:
            print("❌ 没有找到测试日志，说明Native Host没有被调用")
            return False
    
    def run_complete_diagnosis(self):
        """运行完整诊断"""
        print("\n🎯 运行完整诊断")
        print("=" * 60)
        
        results = {}
        
        # 1. Python环境测试
        results['python'] = self.test_python_environment()
        
        # 2. 注册表检查
        results['registry'] = self.check_registry_detailed()
        
        # 3. 批处理文件测试
        results['batch'] = self.test_batch_file_execution()
        
        # 显示结果
        print("\n📊 诊断结果:")
        print("=" * 60)
        for test, result in results.items():
            print(f"   {test}: {'✅' if result else '❌'}")
        
        # 如果有问题，提供最小测试方案
        if not all(results.values()):
            print("\n⚠️ 发现问题，建议使用最小测试配置")
            
            response = input("是否创建并应用最小测试配置? (y/N): ").lower()
            if response == 'y':
                minimal_config = self.create_minimal_test_setup()
                if minimal_config:
                    if self.apply_minimal_config(minimal_config):
                        print("\n✅ 最小测试配置已应用")
                        self.test_edge_connection()
        
        return results

def main():
    print("🎯 Edge2Chrome 终极诊断工具")
    print("=" * 60)
    
    diagnostics = UltimateDiagnostics()
    
    while True:
        print("\n请选择操作:")
        print("1. 运行完整诊断")
        print("2. 检查注册表配置")
        print("3. 测试批处理文件")
        print("4. 创建最小测试配置")
        print("5. 测试Python环境")
        print("0. 退出")
        
        choice = input("\n请输入选项 (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            diagnostics.run_complete_diagnosis()
        elif choice == '2':
            diagnostics.check_registry_detailed()
        elif choice == '3':
            diagnostics.test_batch_file_execution()
        elif choice == '4':
            config = diagnostics.create_minimal_test_setup()
            if config:
                diagnostics.apply_minimal_config(config)
        elif choice == '5':
            diagnostics.test_python_environment()
        else:
            print("❌ 无效选项")
        
        input("\n按Enter继续...")

if __name__ == "__main__":
    main()