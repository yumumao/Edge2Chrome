#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试Edge扩展与Native Host通信问题
"""

import json
import os
import winreg
import subprocess
import sys
import time

def check_extension_config():
    """检查扩展配置"""
    print("🔍 检查扩展配置...")
    
    manifest_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    
    if not os.path.exists(manifest_path):
        print(f"❌ 配置文件不存在: {manifest_path}")
        return False, None
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        allowed_origins = config.get('allowed_origins', [])
        if not allowed_origins:
            print("❌ 没有配置扩展来源")
            return False, None
        
        origin = allowed_origins[0]
        if "你的扩展ID" in origin:
            print("❌ 扩展ID尚未配置")
            return False, None
        
        extension_id = origin.replace("chrome-extension://", "").replace("/", "")
        print(f"✅ 配置的扩展ID: {extension_id}")
        
        return True, extension_id
        
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")
        return False, None

def check_registry():
    """检查注册表"""
    print("\n🔧 检查注册表...")
    
    key_path = r"SOFTWARE\Microsoft\Edge\NativeMessagingHosts\com.edge2chrome.launcher"
    
    for hive_name, hive in [("HKEY_CURRENT_USER", winreg.HKEY_CURRENT_USER)]:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                manifest_path = winreg.QueryValue(key, "")
                print(f"✅ {hive_name}: {manifest_path}")
                return True
        except:
            print(f"❌ {hive_name}: 注册表项不存在")
    
    return False

def test_native_host_directly():
    """直接测试Native Host"""
    print("\n🧪 直接测试Native Host...")
    
    script_path = r"C:\edge2chrome\edge2chrome_launcher.py"
    
    if not os.path.exists(script_path):
        print(f"❌ Native Host脚本不存在: {script_path}")
        return False
    
    try:
        # 准备测试消息
        test_message = {
            "url": "https://www.zhihu.com/test",
            "source": "debug",
            "chromeArgs": "--new-window",
            "timestamp": int(time.time())
        }
        
        print(f"📤 发送测试消息: {test_message}")
        
        # 启动Native Host
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 构造Native Messaging格式的消息
        message_json = json.dumps(test_message)
        message_bytes = message_json.encode('utf-8')
        
        # 构造长度前缀（4字节小端序）
        import struct
        length_bytes = struct.pack('<I', len(message_bytes))
        
        # 发送消息
        full_message = length_bytes + message_bytes
        
        try:
            stdout, stderr = process.communicate(input=message_json, timeout=10)
            
            if process.returncode == 0:
                print("✅ Native Host测试成功")
                if stdout:
                    print(f"📥 输出: {stdout}")
                return True
            else:
                print(f"❌ Native Host返回错误: {process.returncode}")
                if stderr:
                    print(f"错误信息: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            print("⏰ Native Host超时")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def create_test_extension():
    """创建简化的测试扩展"""
    print("\n🔧 创建测试扩展...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(current_dir, "test_extension")
    
    try:
        os.makedirs(test_dir, exist_ok=True)
        
        # 简化的manifest
        test_manifest = {
            "manifest_version": 3,
            "name": "Edge2Chrome Test",
            "version": "1.0.0",
            "permissions": ["nativeMessaging"],
            "background": {
                "service_worker": "test_background.js"
            }
        }
        
        # 简化的background script
        test_background = '''
console.log("Test extension loaded");

chrome.runtime.onInstalled.addListener(() => {
    console.log("Test extension installed");
    
    // 测试Native Host连接
    try {
        const port = chrome.runtime.connectNative('com.edge2chrome.launcher');
        
        port.onMessage.addListener((response) => {
            console.log("Native Host响应:", response);
        });
        
        port.onDisconnect.addListener(() => {
            console.log("Native Host断开连接");
            if (chrome.runtime.lastError) {
                console.error("连接错误:", chrome.runtime.lastError);
            }
        });
        
        // 发送测试消息
        const testMessage = {
            url: "https://www.zhihu.com/test-from-extension",
            source: "test-extension",
            chromeArgs: "--new-window",
            timestamp: Date.now()
        };
        
        console.log("发送测试消息:", testMessage);
        port.postMessage(testMessage);
        
    } catch (error) {
        console.error("连接Native Host失败:", error);
    }
});
'''
        
        # 写入文件
        with open(os.path.join(test_dir, "manifest.json"), 'w', encoding='utf-8') as f:
            json.dump(test_manifest, f, indent=2)
        
        with open(os.path.join(test_dir, "test_background.js"), 'w', encoding='utf-8') as f:
            f.write(test_background)
        
        print(f"✅ 测试扩展创建完成: {test_dir}")
        print("\n📋 加载测试扩展:")
        print("1. 打开 edge://extensions/")
        print("2. 启用开发者模式")
        print("3. 点击'加载解压缩的扩展'")
        print(f"4. 选择文件夹: {test_dir}")
        print("5. 按F12打开开发者工具查看控制台输出")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建测试扩展失败: {e}")
        return False

def main():
    print("🔍 Edge2Chrome 通信诊断工具")
    print("=" * 60)
    
    # 检查配置
    config_ok, extension_id = check_extension_config()
    registry_ok = check_registry()
    native_ok = test_native_host_directly()
    
    print("\n" + "=" * 60)
    print("📊 诊断结果:")
    print(f"   扩展配置: {'✅' if config_ok else '❌'}")
    print(f"   注册表: {'✅' if registry_ok else '❌'}")
    print(f"   Native Host: {'✅' if native_ok else '❌'}")
    
    if not config_ok:
        print("\n❌ 扩展ID配置有问题")
        print("请运行: python config_extension_id.py")
    elif not registry_ok:
        print("\n❌ 注册表配置有问题")
        print("请重新运行: python install_edge.py")
    elif not native_ok:
        print("\n❌ Native Host程序有问题")
        print("请检查Python环境和Chrome路径")
    else:
        print("\n✅ 基础配置都正常")
        
        response = input("\n是否创建测试扩展进行进一步诊断? (y/N): ").lower()
        if response == 'y':
            create_test_extension()
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()