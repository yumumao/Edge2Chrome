#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge2Chrome Native Host (Edge终极适配版)
解决Edge Native Messaging响应接收问题
"""

import json
import sys
import struct
import subprocess
import os
import logging
import time
import signal

# Windows二进制模式
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
    log_dir = r"D:\work\Edge2Chrome\logs"
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "edge_ultimate.log")
        
        # 清空旧日志
        with open(log_file, 'w') as f:
            pass
        
        # 同时输出到文件和stderr
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stderr)
            ]
        )
        
        logging.info("Edge2Chrome Native Host (Edge终极适配版) 启动")
        logging.info(f"Python: {sys.version}")
        logging.info(f"PID: {os.getpid()}")
        
    except Exception as e:
        print(f"日志设置失败: {e}", file=sys.stderr)

def read_input():
    """读取Edge输入 - 兼容版"""
    try:
        logging.debug("开始读取Edge消息...")
        
        # 读取长度（4字节）
        length_data = sys.stdin.buffer.read(4)
        
        if not length_data:
            logging.info("输入流结束")
            return None
        
        if len(length_data) < 4:
            logging.error(f"长度数据不完整: {len(length_data)}")
            return None
        
        # 解析长度
        message_length = struct.unpack('<I', length_data)[0]
        logging.debug(f"消息长度: {message_length}")
        
        if message_length <= 0 or message_length > 1048576:  # 1MB限制
            logging.error(f"消息长度异常: {message_length}")
            return None
        
        # 分块读取消息内容
        message_data = b''
        remaining = message_length
        
        while remaining > 0:
            chunk_size = min(remaining, 4096)
            chunk = sys.stdin.buffer.read(chunk_size)
            
            if not chunk:
                logging.error("消息读取中断")
                return None
            
            message_data += chunk
            remaining -= len(chunk)
        
        logging.debug(f"成功读取消息: {len(message_data)} 字节")
        
        # 解码和解析
        try:
            message_text = message_data.decode('utf-8')
            logging.debug(f"消息内容: {message_text}")
            
            message = json.loads(message_text)
            logging.info(f"解析后的消息: {message}")
            
            return message
            
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logging.error(f"消息解析失败: {e}")
            return None
            
    except Exception as e:
        logging.error(f"读取输入异常: {e}")
        return None

def send_output(message):
    """发送输出到Edge - 强化版"""
    try:
        logging.debug(f"准备发送响应: {message}")
        
        # 序列化
        response_json = json.dumps(message, ensure_ascii=False)
        response_bytes = response_json.encode('utf-8')
        response_length = len(response_bytes)
        
        logging.debug(f"响应JSON: {response_json}")
        logging.debug(f"响应长度: {response_length}")
        
        # 构造完整消息
        length_prefix = struct.pack('<I', response_length)
        full_response = length_prefix + response_bytes
        
        # 原子性写入
        bytes_written = 0
        total_bytes = len(full_response)
        
        while bytes_written < total_bytes:
            try:
                chunk = full_response[bytes_written:]
                written = sys.stdout.buffer.write(chunk)
                
                if written is None:
                    written = len(chunk)
                
                bytes_written += written
                
                # 立即刷新
                sys.stdout.buffer.flush()
                
                logging.debug(f"写入进度: {bytes_written}/{total_bytes}")
                
            except Exception as e:
                logging.error(f"写入失败: {e}")
                break
        
        # 最终刷新
        try:
            sys.stdout.buffer.flush()
            sys.stdout.flush()
            os.fsync(sys.stdout.fileno())  # 强制刷新到OS
        except:
            pass
        
        logging.info(f"响应发送完成: {bytes_written}/{total_bytes} 字节")
        
        # 给Edge时间处理响应
        time.sleep(0.1)
        
        return bytes_written == total_bytes
        
    except Exception as e:
        logging.error(f"发送输出异常: {e}")
        return False

def find_chrome():
    """查找Chrome"""
    for path in CHROME_PATHS:
        if os.path.exists(path):
            logging.info(f"找到Chrome: {path}")
            return path
    
    logging.error("未找到Chrome")
    return None

def launch_chrome(url, args="--new-window"):
    """启动Chrome"""
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
        
        # 启动Chrome
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=False,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        )
        
        # 确保进程启动
        time.sleep(0.2)
        
        logging.info(f"Chrome启动成功, PID: {process.pid}")
        
        return {
            "success": True,
            "message": "Chrome启动成功",
            "url": url,
            "pid": process.pid,
            "chrome_path": chrome_path,
            "timestamp": int(time.time())
        }
        
    except Exception as e:
        error_msg = f"启动Chrome失败: {e}"
        logging.error(error_msg)
        return {"success": False, "error": error_msg}

def signal_handler(signum, frame):
    """信号处理器"""
    logging.info(f"收到信号 {signum}，准备退出")
    sys.exit(0)

def main():
    """主程序 - Edge终极适配版"""
    setup_logging()
    
    # 设置信号处理
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        logging.info("进入Edge终极适配主循环")
        
        # Edge通常只发送一个消息
        message = read_input()
        
        if message is None:
            logging.warning("未收到有效消息")
            # 发送错误响应
            error_response = {
                "success": False,
                "error": "未收到有效消息"
            }
            send_output(error_response)
            return
        
        # 处理消息
        if isinstance(message, dict) and "url" in message:
            url = message["url"]
            chrome_args = message.get("chromeArgs", "--new-window")
            source = message.get("source", "unknown")
            
            logging.info(f"处理来自 {source} 的请求: {url}")
            
            # 启动Chrome
            result = launch_chrome(url, chrome_args)
            
            # 发送响应
            success = send_output(result)
            
            if success:
                logging.info("响应发送成功，程序即将退出")
            else:
                logging.error("响应发送失败")
                
        else:
            logging.warning(f"无效消息格式: {message}")
            error_response = {
                "success": False,
                "error": "无效的消息格式"
            }
            send_output(error_response)
        
        # Edge Native Host在处理完一个消息后应该退出
        logging.info("消息处理完成，正常退出")
        
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
            send_output(error_response)
        except:
            pass
    
    finally:
        logging.info("程序结束")
        # 确保输出完全刷新
        try:
            sys.stdout.buffer.flush()
            sys.stdout.flush()
            if hasattr(os, 'fsync'):
                os.fsync(sys.stdout.fileno())
        except:
            pass

if __name__ == "__main__":
    main()