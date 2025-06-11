#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 深度诊断工具
专门诊断Native Host未被调用的问题
"""

import os
import json
import winreg
import subprocess
import sys
import time
from pathlib import Path

class DeepDiagnosis:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.project_root = self.script_dir.parent
        self.extension_id = "bekgmlladkakjohmhaekpmbiobcggpnb"
        
    def check_extension_id_in_edge(self):
        """检查Edge中的扩展ID"""
        print("\n🔍 检查Edge扩展ID")
        print("=" * 50)
        
        print("📋 请按以下步骤检查扩展ID:")
        print("1. 打开Edge浏览器")
        print("2. 访问 edge://extensions/")
        print("3. 找到 Edge2Chrome 扩展")
        print("4. 点击'详细信息'")
        print("5. 查看扩展ID")
        print()
        
        current_id = input(f"请输入在Edge中看到的实际扩展ID (当前配置: {self.extension_id}): ").strip()
        
        if current_id and current_id != self.extension_id:
            print(f"⚠️ 扩展ID不匹配!")
            print(f"配置中的ID: {self.extension_id}")
            print(f"实际的ID: {current_id}")
            
            response = input("是否更新配置文件中的扩展ID? (y/N): ").lower()
            if response == 'y':
                self.extension_id = current_id
                return self.update_extension_id(current_id)
        elif current_id == self.extension_id:
            print("✅ 扩展ID匹配")
            return True
        else:
            print("⚠️ 未提供扩展ID，继续使用当前配置")
            return True
        
        return False
    
    def update_extension_id(self, new_id):
        """更新扩展ID"""
        try:
            # 更新配置文件
            config_files = [
                "com.edge2chrome.launcher.json",
                "minimal_config.json"
            ]
            
            for config_file in config_files:
                config_path = self.project_root / config_file
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    config['allowed_origins'] = [f"chrome-extension://{new_id}/"]
                    
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ 更新配置文件: {config_file}")
            
            # 更新注册表
            key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
            config_path = self.project_root / "com.edge2chrome.launcher.json"
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, str(config_path))
            
            print("✅ 更新注册表")
            return True
            
        except Exception as e:
            print(f"❌ 更新扩展ID失败: {e}")
            return False
    
    def check_edge_developer_mode(self):
        """检查Edge开发者模式"""
        print("\n🔍 检查Edge开发者模式")
        print("=" * 50)
        
        print("📋 请确认Edge扩展设置:")
        print("1. 访问 edge://extensions/")
        print("2. 确认左下角'开发人员模式'已开启")
        print("3. 确认 Edge2Chrome 扩展状态为'启用'")
        print("4. 如果扩展显示错误，请点击'重新加载'")
        
        input("确认完成后按Enter继续...")
    
    def check_file_permissions(self):
        """检查文件权限"""
        print("\n🔍 检查文件权限")
        print("=" * 50)
        
        files_to_check = [
            "com.edge2chrome.launcher.json",
            "minimal_test.py",
            "minimal_test.bat"
        ]
        
        all_ok = True
        
        for filename in files_to_check:
            filepath = self.project_root / filename
            
            if filepath.exists():
                try:
                    # 检查读取权限
                    with open(filepath, 'r') as f:
                        f.read(1)
                    print(f"✅ {filename}: 可读取")
                    
                    # 检查执行权限（对于.bat文件）
                    if filename.endswith('.bat'):
                        try:
                            # 测试是否能启动进程
                            proc = subprocess.Popen(
                                f'echo test',
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                            )
                            proc.communicate(timeout=1)
                            print(f"✅ {filename}: 可执行")
                        except:
                            print(f"⚠️ {filename}: 执行权限可能有问题")
                            all_ok = False
                    
                except Exception as e:
                    print(f"❌ {filename}: 权限问题 - {e}")
                    all_ok = False
            else:
                print(f"❌ {filename}: 文件不存在")
                all_ok = False
        
        return all_ok
    
    def create_debug_native_host(self):
        """创建调试版Native Host"""
        print("\n🔧 创建调试版Native Host")
        print("=" * 50)
        
        try:
            # 创建极度简化的调试脚本
            debug_script = f'''#!/usr/bin/env python3
import sys
import os
import time

# 记录启动
start_time = time.strftime("%Y-%m-%d %H:%M:%S")
debug_log = r"{self.project_root}\\debug_native.log"

try:
    with open(debug_log, "w", encoding="utf-8") as log:
        log.write(f"DEBUG: Native Host started at {{start_time}}\\n")
        log.write(f"DEBUG: Python version: {{sys.version}}\\n")
        log.write(f"DEBUG: Working directory: {{os.getcwd()}}\\n")
        log.write(f"DEBUG: Arguments: {{sys.argv}}\\n")
        log.flush()
    
    # 尝试读取stdin
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write("DEBUG: Attempting to read from stdin...\\n")
        log.flush()
    
    # 设置二进制模式
    if sys.platform == "win32":
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    
    # 读取输入
    input_data = sys.stdin.buffer.read(4)
    
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write(f"DEBUG: Read {{len(input_data)}} bytes from stdin\\n")
        if input_data:
            log.write(f"DEBUG: Input data: {{input_data}}\\n")
        log.flush()
    
    # 如果有输入，尝试读取完整消息
    if len(input_data) == 4:
        import struct
        length = struct.unpack('<I', input_data)[0]
        
        with open(debug_log, "a", encoding="utf-8") as log:
            log.write(f"DEBUG: Message length: {{length}}\\n")
            log.flush()
        
        if 0 < length < 1024:
            message_data = sys.stdin.buffer.read(length)
            
            with open(debug_log, "a", encoding="utf-8") as log:
                log.write(f"DEBUG: Message data: {{message_data}}\\n")
                log.flush()
            
            # 发送简单响应
            import json
            response = {{"success": True, "debug": True, "message": "Debug response"}}
            response_json = json.dumps(response)
            response_bytes = response_json.encode('utf-8')
            response_length = struct.pack('<I', len(response_bytes))
            
            sys.stdout.buffer.write(response_length)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()
            
            with open(debug_log, "a", encoding="utf-8") as log:
                log.write(f"DEBUG: Sent response: {{response_json}}\\n")
                log.flush()
    
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write("DEBUG: Script completed normally\\n")
        log.flush()

except Exception as e:
    try:
        with open(debug_log, "a", encoding="utf-8") as log:
            log.write(f"DEBUG: Exception occurred: {{e}}\\n")
            import traceback
            log.write(f"DEBUG: Traceback: {{traceback.format_exc()}}\\n")
            log.flush()
    except:
        pass
'''
            
            # 保存调试脚本
            debug_script_path = self.project_root / "debug_native.py"
            with open(debug_script_path, 'w', encoding='utf-8') as f:
                f.write(debug_script)
            print(f"✅ 创建调试脚本: {debug_script_path}")
            
            # 创建调试批处理文件
            debug_bat_content = f'''@echo off
cd /d "{self.project_root}"
python "debug_native.py"
'''
            
            debug_bat_path = self.project_root / "debug_native.bat"
            with open(debug_bat_path, 'w') as f:
                f.write(debug_bat_content)
            print(f"✅ 创建调试批处理: {debug_bat_path}")
            
            # 创建调试配置
            debug_config = {
                "name": "com.edge2chrome.launcher",
                "description": "Edge2Chrome Debug Native Host",
                "path": str(debug_bat_path),
                "type": "stdio",
                "allowed_origins": [
                    f"chrome-extension://{self.extension_id}/"
                ]
            }
            
            debug_config_path = self.project_root / "debug_config.json"
            with open(debug_config_path, 'w', encoding='utf-8') as f:
                json.dump(debug_config, f, indent=2, ensure_ascii=False)
            print(f"✅ 创建调试配置: {debug_config_path}")
            
            return debug_config_path
            
        except Exception as e:
            print(f"❌ 创建调试Native Host失败: {e}")
            return None
    
    def apply_debug_config(self, config_path):
        """应用调试配置"""
        print(f"\n🔧 应用调试配置")
        
        try:
            # 复制到主配置位置
            main_config = self.project_root / "com.edge2chrome.launcher.json"
            
            # 备份当前配置
            if main_config.exists():
                backup_config = self.project_root / "com.edge2chrome.launcher.json.original"
                import shutil
                shutil.copy2(main_config, backup_config)
                print(f"✅ 备份原配置: {backup_config}")
            
            # 应用调试配置
            import shutil
            shutil.copy2(config_path, main_config)
            print(f"✅ 应用调试配置")
            
            # 更新注册表
            key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, str(main_config))
            print(f"✅ 更新注册表")
            
            return True
            
        except Exception as e:
            print(f"❌ 应用调试配置失败: {e}")
            return False
    
    def test_debug_setup(self):
        """测试调试设置"""
        print("\n🧪 测试调试设置")
        print("=" * 50)
        
        debug_log = self.project_root / "debug_native.log"
        
        # 清除旧日志
        if debug_log.exists():
            debug_log.unlink()
        
        print("📋 请按以下步骤测试:")
        print("1. 重新加载Edge扩展 (edge://extensions/)")
        print("2. 完全重启Edge浏览器")
        print("3. 访问知乎或其他匹配的网站")
        print("4. 点击Chrome按钮")
        print("5. 等待几秒钟")
        
        input("完成测试后按Enter继续...")
        
        # 检查调试日志
        if debug_log.exists():
            print("✅ 找到调试日志!")
            with open(debug_log, 'r', encoding='utf-8') as f:
                content = f.read()
            print("📋 调试日志内容:")
            print("-" * 50)
            print(content)
            print("-" * 50)
            return True
        else:
            print("❌ 没有找到调试日志")
            print("这意味着Edge根本没有尝试启动Native Host")
            return False
    
    def check_edge_policies(self):
        """检查Edge策略"""
        print("\n🔍 检查Edge策略")
        print("=" * 50)
        
        print("📋 检查Edge企业策略:")
        print("1. 访问 edge://policy/")
        print("2. 查找与Native Messaging相关的策略")
        print("3. 特别关注:")
        print("   - NativeMessagingAllowlist")
        print("   - NativeMessagingBlocklist") 
        print("   - ExtensionInstallBlocklist")
        print("   - ExtensionInstallAllowlist")
        
        input("检查完成后按Enter继续...")
        
        has_blocking_policy = input("是否发现任何阻止Native Messaging的策略? (y/N): ").lower()
        
        if has_blocking_policy == 'y':
            print("⚠️ 发现阻止策略!")
            print("请联系系统管理员或:")
            print("1. 添加扩展到允许列表")
            print("2. 添加Native Host到允许列表")
            return False
        else:
            print("✅ 没有发现阻止策略")
            return True

def main():
    print("🔍 Edge2Chrome 深度诊断工具")
    print("=" * 60)
    print("专门诊断Native Host未被调用的问题")
    print()
    
    diagnosis = DeepDiagnosis()
    
    # 步骤1: 检查扩展ID
    print("步骤1: 检查扩展ID匹配")
    extension_id_ok = diagnosis.check_extension_id_in_edge()
    
    # 步骤2: 检查开发者模式
    print("\n步骤2: 检查Edge设置")
    diagnosis.check_edge_developer_mode()
    
    # 步骤3: 检查文件权限
    print("\n步骤3: 检查文件权限")
    permissions_ok = diagnosis.check_file_permissions()
    
    # 步骤4: 检查Edge策略
    print("\n步骤4: 检查Edge策略")
    policies_ok = diagnosis.check_edge_policies()
    
    # 步骤5: 创建和测试调试版本
    print("\n步骤5: 创建调试版Native Host")
    debug_config = diagnosis.create_debug_native_host()
    
    if debug_config:
        if diagnosis.apply_debug_config(debug_config):
            print("\n步骤6: 测试调试版本")
            debug_result = diagnosis.test_debug_setup()
            
            if debug_result:
                print("\n🎉 调试成功!")
                print("Native Host能够被调用，问题可能在于原始脚本的逻辑")
            else:
                print("\n❌ 调试失败")
                print("Edge确实无法调用Native Host")
                print("\n可能的原因:")
                print("1. 扩展ID不匹配")
                print("2. Edge企业策略阻止")
                print("3. Edge版本兼容性问题")
                print("4. 系统权限问题")
    
    print("\n📊 诊断总结:")
    print(f"   扩展ID: {'✅' if extension_id_ok else '❌'}")
    print(f"   文件权限: {'✅' if permissions_ok else '❌'}")
    print(f"   Edge策略: {'✅' if policies_ok else '❌'}")
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()