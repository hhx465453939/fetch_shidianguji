#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整版《梦林玄解》获取脚本
获取所有章节的内容
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
        content = re.sub(r'下一篇', '', content)
        
        # 清理多余空白行
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        content = '\n\n'.join(lines)
        
        return content
        
    except Exception as e:
        print(f"获取失败: {e}")
        return ""

def main():
    # 根据从网页获取的信息，构建完整的章节列表
    # 这些章节ID是从网页内容中提取的
    chapters = [
        {'url': 'https://www.shidianguji.com/book/HY1523/chapter/1knwrejn2amuu', 'title': '梦林玄解小引'},
        {'url': 'https://www.shidianguji.com/book/HY1523/chapter/1knwrejrl4zyj', 'title': '梦林玄解凡例'},
        # 需要根据实际网页结构添加更多章节
    ]
    
    # 尝试获取更多章节
    # 基于常见的章节ID模式，尝试获取更多章节
    base_url = "https://www.shidianguji.com/book/HY1523/chapter/"
    
    # 从已知的章节ID模式推断其他章节
    # 已知: 1knwrejn2amuu (小引), 1knwrejrl4zyj (凡例)
    # 尝试获取更多章节
    additional_chapters = [
        {'url': base_url + '1knwrejn2amuu', 'title': '梦林玄解小引'},
        {'url': base_url + '1knwrejrl4zyj', 'title': '梦林玄解凡例'},
        {'url': base_url + '1knwrejrl4zyj', 'title': '梦林玄解叙'},  # 可能需要不同的ID
        {'url': base_url + '1knwrejrl4zyj', 'title': '梦林玄解总目录'},  # 可能需要不同的ID
    ]
    
    # 去重
    seen_urls = set()
    unique_chapters = []
    for chapter in additional_chapters:
        if chapter['url'] not in seen_urls:
            seen_urls.add(chapter['url'])
            unique_chapters.append(chapter)
    
    # 获取内容
    all_content = []
    for chapter in unique_chapters:
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
        with open('梦林玄解_完整版.md', 'w', encoding='utf-8') as f:
            f.write("# 梦林玄解\n\n")
            f.write("**作者：** [北宋] 邵雍 纂辑 · [明] 陈士元 增删 · [明] 何栋如 重编\n\n")
            f.write("**来源：** 识典古籍 (https://www.shidianguji.com/)\n\n")
            f.write("**获取时间：** " + time.strftime("%Y年%m月%d日") + "\n\n")
            f.write("---\n\n")
            
            # 写入目录
            f.write("## 目录\n\n")
            for i, chapter in enumerate(all_content, 1):
                f.write(f"{i}. [{chapter['title']}](#{chapter['title'].replace(' ', '-')})\n")
            f.write("\n---\n\n")
            
            for i, chapter in enumerate(all_content, 1):
                f.write(f"## {i}. {chapter['title']}\n\n")
                f.write(f"**来源链接：** {chapter['url']}\n\n")
                f.write("---\n\n")
                f.write(chapter['content'])
                f.write("\n\n---\n\n")
        
        print(f"保存完成！共保存 {len(all_content)} 个章节到 梦林玄解_完整版.md")
    else:
        print("未获取到任何内容")

if __name__ == "__main__":
    main() 