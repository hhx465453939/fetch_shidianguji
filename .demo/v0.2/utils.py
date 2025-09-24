#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具类
提供一些通用的辅助函数
"""

import re
import os
import time
from urllib.parse import urlparse

def extract_book_id_from_url(url):
    """从URL中提取书籍ID"""
    if not url:
        return None
        
    # 匹配 /book/HY1523/ 这样的模式
    match = re.search(r'/book/([^/]+)/', url)
    if match:
        return match.group(1)
    return None

def clean_filename(filename):
    """清理文件名，移除不合法字符"""
    # 移除或替换不合法的文件名字符
    illegal_chars = r'[<>:"/\\|?*]'
    cleaned = re.sub(illegal_chars, '_', filename)
    
    # 限制文件名长度
    if len(cleaned) > 100:
        cleaned = cleaned[:100]
    
    return cleaned

def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_url(url):
    """验证URL格式"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def create_output_dir(path):
    """创建输出目录"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False

def safe_sleep(seconds):
    """安全的睡眠函数，带进度提示"""
    if seconds <= 0:
        return
    
    print(f"等待 {seconds} 秒...", end="", flush=True)
    for i in range(seconds):
        time.sleep(1)
        print(".", end="", flush=True)
    print(" 完成")

def print_progress(current, total, prefix="进度"):
    """打印进度信息"""
    percentage = (current / total) * 100 if total > 0 else 0
    print(f"{prefix}: {current}/{total} ({percentage:.1f}%)")

class Timer:
    """简单的计时器类"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """开始计时"""
        self.start_time = time.time()
        return self
    
    def stop(self):
        """停止计时"""
        self.end_time = time.time()
        return self
    
    def elapsed(self):
        """获取经过的时间（秒）"""
        if self.start_time is None:
            return 0
        
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def elapsed_str(self):
        """获取格式化的经过时间"""
        elapsed = self.elapsed()
        
        if elapsed < 60:
            return f"{elapsed:.1f} 秒"
        elif elapsed < 3600:
            minutes = elapsed // 60
            seconds = elapsed % 60
            return f"{int(minutes)} 分 {seconds:.1f} 秒"
        else:
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            return f"{int(hours)} 时 {int(minutes)} 分 {seconds:.1f} 秒" 