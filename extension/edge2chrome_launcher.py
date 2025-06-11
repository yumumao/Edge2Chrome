#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome Native Host
将来自Edge扩展的请求转发给Chrome浏览器
"""

import json
import sys
import struct
import subprocess
import os
import logging
from datetime import datetime
import traceback

# Chrome可执行文件可能的路径
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
    r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe",
]

# 日志设置
def setup_logging():
    log_dir = r"C:\edge2chrome_logs"
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "edge2chrome.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        logging.info("=" * 50)
        logging.info("Edge2Chrome Native Host 启动")
        logging.info("=" * 50)
    except Exception as e:
        # 如果无法创建日志文件，就不记录日志
        pass

def send_message(message):
    """发送消息给Edge扩展"""
    try:
        encoded_content = json.dumps(message, ensure_ascii=False).encode('utf-8')
        encoded_length = struct.pack('<I', len(encoded_content))
        sys.stdout.buffer.write(encoded_length)
        sys.stdout.buffer.write(encoded_content)
        sys.stdout.buffer.flush()
        logging.info(f"发送消息: {message}")
    except Exception as e:
        logging.error(f"发送消息失败: {e}")
        logging.error(traceback.format_exc())

def read_message():
    """从Edge扩展读取消息"""
    try:
        # 读取消息长度（4字节）
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            return None
        
        message_length = struct.unpack('<I', raw_length)[0]
        
        # 读取消息内容
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        parsed_message = json.loads(message)
        logging.info(f"收到消息: {parsed_message}")
        return parsed_message
    except Exception as e:
        logging.error(f"读取消息失败: {e}")
        logging.error(traceback.format_exc())
        send_message({"error": f"读取消息失败: {str(e)}"})
        return None

def find_chrome():
    """查找Chrome可执行文件"""
    for path in CHROME_PATHS:
        if os.path.exists(path):
            logging.info(f"找到Chrome: {path}")
            return path
    
    logging.error("未找到Chrome浏览器")
    return None

def parse_chrome_args(args_string):
    """解析Chrome启动参数"""
    if not args_string:
        return ["--new-window"]
    
    # 简单的参数分割，支持引号
    args = []
    current_arg = ""
    in_quotes = False
    
    for char in args_string:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ' ' and not in_quotes:
            if current_arg:
                args.append(current_arg)
                current_arg = ""
        else:
            current_arg += char
    
    if current_arg:
        args.append(current_arg)
    
    return args if args else ["--new-window"]

def open_chrome(url, chrome_args="--new-window"):
    """使用Chrome打开URL"""
    try:
        chrome_path = find_chrome()
        if not chrome_path:
            return {
                "success": False, 
                "error": "未找到Chrome浏览器，请检查是否已安装Chrome"
            }
        
        # 解析Chrome参数
        args = parse_chrome_args(chrome_args)
        
        # 构建命令行参数
        cmd = [chrome_path] + args + [url]
        
        logging.info(f"执行命令: {' '.join(cmd)}")
        
        # 启动Chrome
        process = subprocess.Popen(
            cmd, 
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        logging.info(f"Chrome进程已启动，PID: {process.pid}")
        
        return {
            "success": True, 
            "message": "已用Chrome打开链接",
            "url": url,
            "chrome_path": chrome_path,
            "chrome_args": args,
            "pid": process.pid
        }
    
    except Exception as e:
        error_msg = f"启动Chrome失败: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        return {"success": False, "error": error_msg}

def main():
    """主程序循环"""
    setup_logging()
    
    try:
        while True:
            message = read_message()
            if message is None:
                break
            
            if "url" in message:
                url = message["url"]
                source = message.get("source", "unknown")
                chrome_args = message.get("chromeArgs", "--new-window")
                timestamp = message.get("timestamp", "")
                
                logging.info(f"处理来自{source}的URL请求: {url}")
                logging.info(f"Chrome参数: {chrome_args}")
                
                result = open_chrome(url, chrome_args)
                send_message(result)
            else:
                error_msg = "无效的消息格式，缺少url字段"
                logging.warning(f"无效消息: {message}")
                send_message({"error": error_msg})
                
    except KeyboardInterrupt:
        logging.info("程序被用户中断")
    except Exception as e:
        error_msg = f"程序错误: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        send_message({"error": error_msg})
    finally:
        logging.info("Edge2Chrome Native Host 结束")

if __name__ == "__main__":
    main()