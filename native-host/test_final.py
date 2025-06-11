#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试工具
"""

import subprocess
import json
import struct
import sys
import os

def test_native_messaging():
    """测试Native Messaging通信"""
    print("🧪 测试Native Messaging通信")
    print("=" * 50)
    
    script_path = r"C:\edge2chrome\edge2chrome_launcher.py"
    
    try:
        # 启动Native Host
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 准备消息
        test_message = {
            "url": "https://www.zhihu.com/test-final",
            "source": "final-test",
            "chromeArgs": "--new-window"
        }
        
        print(f"📤 发送消息: {test_message}")
        
        # 编码消息
        message_json = json.dumps(test_message)
        message_bytes = message_json.encode('utf-8')
        length_bytes = struct.pack('<I', len(message_bytes))
        
        # 发送消息
        process.stdin.write(length_bytes)
        process.stdin.write(message_bytes)
        process.stdin.flush()
        process.stdin.close()
        
        # 读取响应
        try:
            stdout, stderr = process.communicate(timeout=10)
            
            print(f"📥 程序输出: {len(stdout)} 字节")
            print(f"📥 错误输出: {stderr.decode('utf-8') if stderr else '无'}")
            
            if len(stdout) >= 4:
                # 解析响应
                response_length = struct.unpack('<I', stdout[:4])[0]
                if len(stdout) >= 4 + response_length:
                    response_data = stdout[4:4+response_length]
                    response = json.loads(response_data.decode('utf-8'))
                    
                    print(f"📋 响应: {response}")
                    
                    if response.get('success'):
                        print("✅ 测试成功！")
                        return True
                    else:
                        print(f"❌ 测试失败: {response.get('error')}")
                        return False
            else:
                print("❌ 没有收到有效响应")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            print("⏰ 程序响应超时")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def check_config():
    """检查配置"""
    print("\n🔍 检查配置文件")
    print("=" * 50)
    
    config_path = r"C:\edge2chrome\com.edge2chrome.launcher.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📋 当前配置:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        # 检查扩展ID
        origins = config.get('allowed_origins', [])
        if origins:
            expected_id = "bekgmlladkakjohmhaekpmbiobcggpnb"
            if expected_id in origins[0]:
                print(f"✅ 扩展ID配置正确: {expected_id}")
                return True
            else:
                print(f"❌ 扩展ID配置错误")
                return False
        else:
            print("❌ 没有配置扩展来源")
            return False
            
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")
        return False

def main():
    print("🎯 Edge2Chrome 最终测试")
    print("=" * 60)
    
    # 检查配置
    config_ok = check_config()
    
    if not config_ok:
        print("\n❌ 配置有问题，请先修复配置")
        input("按Enter退出...")
        return
    
    # 测试Native Messaging
    test_ok = test_native_messaging()
    
    print("\n" + "=" * 60)
    print("📊 测试结果:")
    print(f"   配置检查: {'✅' if config_ok else '❌'}")
    print(f"   通信测试: {'✅' if test_ok else '❌'}")
    
    if config_ok and test_ok:
        print("\n🎉 所有测试通过！")
        print("现在可以在Edge中测试扩展功能了")
    else:
        print("\n❌ 测试失败，请检查问题")
        
        # 检查日志
        log_path = r"C:\edge2chrome_logs\edge2chrome_final.log"
        if os.path.exists(log_path):
            print(f"\n📋 查看详细日志: {log_path}")
    
    input("\n按Enter退出...")

if __name__ == "__main__":
    main()