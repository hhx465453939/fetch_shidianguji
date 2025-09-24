#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版《梦林玄解》获取脚本
直接获取已知章节的内容
"""

import requests
import time
from bs4 import BeautifulSoup
import re

def get_chapter_content(url, title):
    """获取章节内容"""
    print(f"正在获取: {title}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 移除脚本和样式
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取文本内容
        content = soup.get_text(separator='\n', strip=True)
        
        # 清理内容
        content = re.sub(r'识典古籍.*?版权所有', '', content, flags=re.DOTALL)
        content = re.sub(r'登录后阅读更方便', '', content)
        content = re.sub(r'书库', '', content)
        
        # 清理多余空白行
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        content = '\n\n'.join(lines)
        
        return content
        
    except Exception as e:
        print(f"获取失败: {e}")
        return ""

def main():
    # 已知的章节
    chapters = [
        {
            'url': 'https://www.shidianguji.com/book/HY1523/chapter/1knwrejn2amuu',
            'title': '梦林玄解小引'
        },
        {
            'url': 'https://www.shidianguji.com/book/HY1523/chapter/1knwrejrl4zyj',
            'title': '梦林玄解凡例'
        }
    ]
    
    # 获取内容
    all_content = []
    for chapter in chapters:
        content = get_chapter_content(chapter['url'], chapter['title'])
        if content:
            all_content.append({
                'title': chapter['title'],
                'url': chapter['url'],
                'content': content
            })
        time.sleep(1)  # 避免请求过快
    
    # 保存为markdown
    if all_content:
        with open('梦林玄解.md', 'w', encoding='utf-8') as f:
            f.write("# 梦林玄解\n\n")
            f.write("**作者：** [北宋] 邵雍 纂辑 · [明] 陈士元 增删 · [明] 何栋如 重编\n\n")
            f.write("**来源：** 识典古籍 (https://www.shidianguji.com/)\n\n")
            f.write("---\n\n")
            
            for i, chapter in enumerate(all_content, 1):
                f.write(f"## {i}. {chapter['title']}\n\n")
                f.write(f"**来源链接：** {chapter['url']}\n\n")
                f.write("---\n\n")
                f.write(chapter['content'])
                f.write("\n\n---\n\n")
        
        print(f"保存完成！共保存 {len(all_content)} 个章节")
    else:
        print("未获取到任何内容")

if __name__ == "__main__":
    main() 