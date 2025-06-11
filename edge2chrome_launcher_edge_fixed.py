#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome Native Host (Edge修复版)
解决Edge Native Messaging通信问题
"""

import json
import sys
import struct
import subprocess
import os
import logging
import time
import threading

# Windows二进制模式设置
if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
]

def setup_logging():
    """设置日志"""
    log_dir = r"D:\\work\\Edge2Chrome\logs"
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "edge_fixed.log")
        
        # 清空旧日志
        with open(log_file, 'w') as f:
            pass
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stderr)  # 同时输出到stderr用于调试
            ]
        )
        
        logging.info("Edge2Chrome Native Host (Edge修复版) 启动")
        logging.info(f"Python: {sys.version}")
        logging.info(f"工作目录: {os.getcwd()}")
        
    except Exception as e:
        # 即使日志失败也要继续运行
        print(f"日志设置失败: {e}", file=sys.stderr)

def read_message_safe():
    """安全读取消息 - Edge兼容版"""
    try:
        logging.debug("开始读取消息...")
        
        # 读取消息长度（4字节小端序）
        length_data = sys.stdin.buffer.read(4)
        
        if not length_data:
            logging.info("收到EOF，连接关闭")
            return None
        
        if len(length_data) < 4:
            logging.error(f"长度数据不完整: {len(length_data)} 字节")
            return None
        
        # 解析消息长度
        message_length = struct.unpack('<I', length_data)[0]
        logging.debug(f"消息长度: {message_length}")
        
        if message_length <= 0:
            logging.warning("消息长度为0")
            return None
        
        if message_length > 1024 * 1024:  # 1MB限制
            logging.error(f"消息长度过大: {message_length}")
            return None
        
        # 读取消息内容
        message_data = b''
        bytes_to_read = message_length
        
        while bytes_to_read > 0:
            chunk = sys.stdin.buffer.read(bytes_to_read)
            if not chunk:
                logging.error("消息读取中断")
                return None
            message_data += chunk
            bytes_to_read -= len(chunk)
        
        logging.debug(f"成功读取 {len(message_data)} 字节消息数据")
        
        # 解码消息
        try:
            message_text = message_data.decode('utf-8')
            logging.debug(f"消息文本: {message_text}")
        except UnicodeDecodeError as e:
            logging.error(f"消息解码失败: {e}")
            return None
        
        # 解析JSON
        try:
            message = json.loads(message_text)
            logging.info(f"收到消息: {message}")
            return message
        except json.JSONDecodeError as e:
            logging.error(f"JSON解析失败: {e}")
            logging.error(f"原始消息: {repr(message_text)}")
            return None
            
    except Exception as e:
        logging.error(f"读取消息异常: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None

def send_message_safe(message):
    """安全发送消息 - Edge兼容版"""
    try:
        logging.debug(f"准备发送消息: {message}")
        
        # 序列化消息
        message_json = json.dumps(message, ensure_ascii=False)
        message_bytes = message_json.encode('utf-8')
        message_length = len(message_bytes)
        
        logging.debug(f"消息JSON: {message_json}")
        logging.debug(f"消息字节长度: {message_length}")
        
        # 构造长度前缀（4字节小端序）
        length_bytes = struct.pack('<I', message_length)
        
        # 原子性写入 - 防止Edge读取中断
        full_message = length_bytes + message_bytes
        
        # 写入到stdout
        bytes_written = 0
        while bytes_written < len(full_message):
            chunk = full_message[bytes_written:]
            try:
                written = sys.stdout.buffer.write(chunk)
                if written is None:
                    written = len(chunk)
                bytes_written += written
                sys.stdout.buffer.flush()
            except Exception as e:
                logging.error(f"写入失败: {e}")
                break
        
        logging.info(f"消息发送完成: 总长度={len(full_message)}, 已写入={bytes_written}")
        
        # 确保数据刷新
        try:
            sys.stdout.buffer.flush()
            sys.stdout.flush()
        except:
            pass
        
        return True
        
    except Exception as e:
        logging.error(f"发送消息异常: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False

def find_chrome():
    """查找Chrome"""
    for path in CHROME_PATHS:
        if os.path.exists(path):
            logging.info(f"找到Chrome: {path}")
            return path
    
    logging.error("未找到Chrome")
    return None

def launch_chrome_safe(url, args="--new-window"):
    """安全启动Chrome"""
    try:
        chrome_path = find_chrome()
        if not chrome_path:
            return {"success": False, "error": "未找到Chrome浏览器"}
        
        # 处理参数
        if isinstance(args, str):
            chrome_args = [arg.strip() for arg in args.split() if arg.strip()]
        else:
            chrome_args = ["--new-window"]
        
        if not chrome_args:
            chrome_args = ["--new-window"]
        
        # 构建命令
        cmd = [chrome_path] + chrome_args + [url]
        logging.info(f"执行命令: {cmd}")
        
        # 启动Chrome进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=False,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        )
        
        # 短暂等待确保进程启动
        time.sleep(0.2)
        
        # 检查进程状态
        poll_result = process.poll()
        if poll_result is not None:
            logging.warning(f"Chrome进程立即退出，返回码: {poll_result}")
        
        logging.info(f"Chrome启动成功, PID: {process.pid}")
        
        return {
            "success": True,
            "message": "Chrome启动成功",
            "url": url,
            "pid": process.pid,
            "chrome_path": chrome_path,
            "chrome_args": chrome_args
        }
        
    except Exception as e:
        error_msg = f"启动Chrome失败: {e}"
        logging.error(error_msg)
        import traceback
        logging.error(traceback.format_exc())
        return {"success": False, "error": error_msg}

def main():
    """主程序 - Edge兼容版"""
    setup_logging()
    
    try:
        logging.info("进入Edge兼容主循环")
        
        # 处理第一个消息
        message = read_message_safe()
        
        if message is None:
            logging.warning("没有收到有效消息")
            return
        
        # 处理消息
        if isinstance(message, dict) and "url" in message:
            url = message["url"]
            chrome_args = message.get("chromeArgs", "--new-window")
            source = message.get("source", "unknown")
            
            logging.info(f"处理来自 {source} 的URL请求: {url}")
            
            # 启动Chrome
            result = launch_chrome_safe(url, chrome_args)
            
            # 发送响应
            send_success = send_message_safe(result)
            
            if send_success:
                logging.info("响应发送成功")
            else:
                logging.error("响应发送失败")
                
        else:
            logging.warning(f"无效消息格式: {message}")
            error_response = {
                "success": False,
                "error": "无效的消息格式，需要包含url字段"
            }
            send_message_safe(error_response)
        
        # Edge的Native Host通常处理一个消息后就退出
        logging.info("消息处理完成，准备退出")
        
    except KeyboardInterrupt:
        logging.info("程序被中断")
    except Exception as e:
        logging.error(f"主程序异常: {e}")
        import traceback
        logging.error(traceback.format_exc())
        
        # 尝试发送错误响应
        try:
            error_response = {
                "success": False,
                "error": f"程序异常: {e}"
            }
            send_message_safe(error_response)
        except:
            pass
    finally:
        logging.info("程序结束")
        # 确保所有输出都刷新
        try:
            sys.stdout.buffer.flush()
            sys.stdout.flush()
            sys.stderr.flush()
        except:
            pass

if __name__ == "__main__":
    main()