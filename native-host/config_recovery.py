#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome 配置恢复工具
恢复到能够调用Native Host的工作状态
"""

import os
import json
import winreg
import shutil
from pathlib import Path

class ConfigRecovery:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.project_root = self.script_dir.parent
        self.extension_id = "bekgmlladkakjohmhaekpmbiobcggpnb"
        
    def list_available_configs(self):
        """列出所有可用的配置文件"""
        print("\n📋 可用的配置文件:")
        print("=" * 50)
        
        configs = []
        config_patterns = [
            "com.edge2chrome.launcher.json",
            "com.edge2chrome.launcher.json.backup", 
            "com.edge2chrome.launcher.json.original",
            "minimal_config.json",
            "debug_config.json",
            "test_config.json"
        ]
        
        for pattern in config_patterns:
            config_path = self.project_root / pattern
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    path = config.get('path', 'N/A')
                    description = config.get('description', 'N/A')
                    origins = config.get('allowed_origins', [])
                    
                    configs.append({
                        'file': pattern,
                        'path_obj': config_path,
                        'config': config,
                        'bat_path': path,
                        'description': description,
                        'origins': origins
                    })
                    
                    print(f"✅ {pattern}")
                    print(f"   描述: {description}")
                    print(f"   批处理: {path}")
                    print(f"   允许来源: {origins}")
                    print(f"   批处理文件存在: {'✅' if os.path.exists(path) else '❌'}")
                    print()
                    
                except Exception as e:
                    print(f"❌ {pattern}: 读取失败 - {e}")
        
        return configs
    
    def list_available_scripts(self):
        """列出所有可用的Python脚本"""
        print("\n📋 可用的Python脚本:")
        print("=" * 50)
        
        scripts = []
        script_patterns = [
            "edge2chrome_launcher.py",
            "edge2chrome_launcher_edge.py", 
            "edge2chrome_launcher_edge_fixed.py",
            "edge2chrome_launcher_edge_ultimate.py",
            "minimal_test.py",
            "debug_native.py"
        ]
        
        for pattern in script_patterns:
            script_path = self.project_root / pattern
            if script_path.exists():
                size = script_path.stat().st_size
                scripts.append({
                    'file': pattern,
                    'path': script_path,
                    'size': size
                })
                
                print(f"✅ {pattern} ({size} 字节)")
        
        return scripts
    
    def create_working_config(self):
        """创建已知可工作的配置（基于你之前的成功日志）"""
        print("\n🔧 创建已知可工作的配置")
        print("=" * 50)
        
        try:
            # 根据你之前的成功日志，使用 edge2chrome_launcher_edge_fixed.py
            working_script = "edge2chrome_launcher_edge_fixed.py"
            working_script_path = self.project_root / working_script
            
            # 如果脚本不存在，创建一个简化的工作版本
            if not working_script_path.exists():
                print(f"⚠️ {working_script} 不存在，创建简化版本...")
                
                working_script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome Native Host (简化工作版)
基于之前成功的配置
"""

import json
import sys
import struct
import subprocess
import os
import logging
import time

# Windows二进制模式
if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

def setup_logging():
    """设置日志"""
    log_dir = r"D:\\work\\Edge2Chrome\\logs"
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "working_version.log")
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8')
            ]
        )
        
        logging.info("Edge2Chrome Native Host (简化工作版) 启动")
        
    except Exception as e:
        pass

def main():
    """主程序"""
    setup_logging()
    
    try:
        logging.info("进入主循环")
        
        # 读取长度
        length_data = sys.stdin.buffer.read(4)
        if len(length_data) == 4:
            length = struct.unpack('<I', length_data)[0]
            logging.debug(f"消息长度: {length}")
            
            # 读取消息
            message_data = sys.stdin.buffer.read(length)
            message = json.loads(message_data.decode('utf-8'))
            logging.info(f"收到消息: {message}")
            
            # 启动Chrome
            url = message.get("url", "")
            chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            
            if os.path.exists(chrome_path) and url:
                cmd = [chrome_path, "--new-window", url]
                logging.info(f"执行命令: {cmd}")
                
                process = subprocess.Popen(cmd, shell=False)
                logging.info(f"Chrome启动成功, PID: {process.pid}")
                
                # 发送响应
                response = {
                    "success": True,
                    "message": "Chrome启动成功",
                    "url": url,
                    "pid": process.pid
                }
            else:
                response = {"success": False, "error": "Chrome not found or no URL"}
            
            # 发送响应
            response_json = json.dumps(response)
            response_bytes = response_json.encode('utf-8')
            length_bytes = struct.pack('<I', len(response_bytes))
            
            sys.stdout.buffer.write(length_bytes)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()
            
            logging.info(f"响应发送成功: {response}")
        
    except Exception as e:
        logging.error(f"程序异常: {e}")

if __name__ == "__main__":
    main()
'''
                
                with open(working_script_path, 'w', encoding='utf-8') as f:
                    f.write(working_script_content)
                print(f"✅ 创建工作脚本: {working_script_path}")
            
            # 创建对应的批处理文件
            working_bat = "edge2chrome_launcher_edge_fixed.bat"
            working_bat_path = self.project_root / working_bat
            
            bat_content = f'''@echo off
cd /d "{self.project_root}"
python "{working_script}"
'''
            
            with open(working_bat_path, 'w') as f:
                f.write(bat_content)
            print(f"✅ 创建工作批处理: {working_bat_path}")
            
            # 创建工作配置
            working_config = {
                "name": "com.edge2chrome.launcher",
                "description": "Edge2Chrome Native Host (Working Version)",
                "path": str(working_bat_path),
                "type": "stdio",
                "allowed_origins": [
                    f"chrome-extension://{self.extension_id}/"
                ]
            }
            
            working_config_path = self.project_root / "working_config.json"
            with open(working_config_path, 'w', encoding='utf-8') as f:
                json.dump(working_config, f, indent=2, ensure_ascii=False)
            print(f"✅ 创建工作配置: {working_config_path}")
            
            return working_config_path
            
        except Exception as e:
            print(f"❌ 创建工作配置失败: {e}")
            return None
    
    def apply_config(self, config_path):
        """应用指定配置"""
        print(f"\n🔧 应用配置: {config_path}")
        
        try:
            # 读取配置
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 备份当前配置
            current_config = self.project_root / "com.edge2chrome.launcher.json"
            if current_config.exists():
                backup_time = int(time.time())
                backup_config = self.project_root / f"com.edge2chrome.launcher.json.backup_{backup_time}"
                shutil.copy2(current_config, backup_config)
                print(f"✅ 备份当前配置: {backup_config}")
            
            # 应用新配置
            shutil.copy2(config_path, current_config)
            print(f"✅ 应用新配置")
            
            # 更新注册表
            key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, str(current_config))
            print(f"✅ 更新注册表")
            
            # 验证批处理文件存在
            bat_path = config.get('path', '')
            if os.path.exists(bat_path):
                print(f"✅ 批处理文件存在: {bat_path}")
            else:
                print(f"⚠️ 批处理文件不存在: {bat_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ 应用配置失败: {e}")
            return False
    
    def restore_original_background(self):
        """恢复原始background.js"""
        print("\n🔧 恢复原始background.js")
        print("=" * 50)
        
        # 检查是否有备份
        background_path = self.project_root / "extension" / "background.js"
        backup_path = self.project_root / "extension" / "background.js.backup"
        
        if backup_path.exists():
            try:
                shutil.copy2(backup_path, background_path)
                print(f"✅ 恢复background.js从备份")
                return True
            except Exception as e:
                print(f"❌ 恢复失败: {e}")
        else:
            print("⚠️ 没有找到background.js备份")
            
            # 创建一个简单的working版本
            simple_background = '''// Edge2Chrome Background Script (简化版)
console.log('[Edge2Chrome] 简化版Background Script启动');

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Edge2Chrome] 收到请求:', request);
  
  if (request.action === 'openInChrome') {
    console.log('[Edge2Chrome] 处理Chrome请求:', request.url);
    
    try {
      const nativePort = chrome.runtime.connectNative('com.edge2chrome.launcher');
      
      let responseHandled = false;
      
      const timeout = setTimeout(() => {
        if (!responseHandled) {
          responseHandled = true;
          console.error('[Edge2Chrome] Native Host超时');
          sendResponse({
            success: false,
            error: 'Native Host响应超时'
          });
          try { nativePort.disconnect(); } catch(e) {}
        }
      }, 5000);
      
      nativePort.onMessage.addListener((response) => {
        console.log('[Edge2Chrome] 收到响应:', response);
        if (!responseHandled) {
          responseHandled = true;
          clearTimeout(timeout);
          sendResponse({
            success: true,
            response: response
          });
          try { nativePort.disconnect(); } catch(e) {}
        }
      });
      
      nativePort.onDisconnect.addListener(() => {
        console.log('[Edge2Chrome] 连接断开');
        if (!responseHandled) {
          responseHandled = true;
          clearTimeout(timeout);
          
          let errorMsg = 'Native Host连接断开';
          if (chrome.runtime.lastError) {
            errorMsg = chrome.runtime.lastError.message;
          }
          
          sendResponse({
            success: false,
            error: errorMsg
          });
        }
      });
      
      const message = {
        url: request.url,
        source: 'edge-simple',
        chromeArgs: request.chromeArgs || '--new-window',
        timestamp: Date.now()
      };
      
      console.log('[Edge2Chrome] 发送消息:', message);
      nativePort.postMessage(message);
      
    } catch (error) {
      console.error('[Edge2Chrome] 连接异常:', error);
      sendResponse({
        success: false,
        error: error.message
      });
    }
    
    return true;
  }
  
  return false;
});

console.log('[Edge2Chrome] 简化版Background Script加载完成');
'''
            
            try:
                with open(background_path, 'w', encoding='utf-8') as f:
                    f.write(simple_background)
                print(f"✅ 创建简化版background.js")
                return True
            except Exception as e:
                print(f"❌ 创建简化版background.js失败: {e}")
        
        return False
    
    def run_recovery(self):
        """运行完整恢复"""
        print("\n🚀 Edge2Chrome 配置恢复")
        print("=" * 60)
        
        # 1. 列出可用配置
        configs = self.list_available_configs()
        scripts = self.list_available_scripts()
        
        # 2. 创建工作配置
        print("\n选择恢复方案:")
        print("1. 使用现有配置文件")
        print("2. 创建已知可工作的配置")
        print("3. 恢复原始background.js")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == '1' and configs:
            print("\n可用配置:")
            for i, config in enumerate(configs):
                print(f"{i+1}. {config['file']} - {config['description']}")
            
            try:
                config_choice = int(input("选择配置 (1-{}): ".format(len(configs)))) - 1
                if 0 <= config_choice < len(configs):
                    selected_config = configs[config_choice]
                    self.apply_config(selected_config['path_obj'])
                    print("\n✅ 配置恢复完成!")
                else:
                    print("❌ 无效选择")
            except ValueError:
                print("❌ 无效输入")
                
        elif choice == '2':
            working_config = self.create_working_config()
            if working_config:
                self.apply_config(working_config)
                print("\n✅ 工作配置创建并应用完成!")
            
        elif choice == '3':
            self.restore_original_background()
            print("\n✅ background.js恢复完成!")
        
        print("\n📋 下一步操作:")
        print("1. 重新加载Edge扩展 (edge://extensions/)")
        print("2. 完全重启Edge浏览器") 
        print("3. 测试扩展功能")
        print("4. 查看日志文件验证Native Host是否被调用")

def main():
    recovery = ConfigRecovery()
    recovery.run_recovery()
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()