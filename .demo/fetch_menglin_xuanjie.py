#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《梦林玄解》批量下载脚本
从识典古籍网站获取《梦林玄解》的所有章节内容并保存为markdown格式
"""

import requests
import time
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

class MenglinXuanjieFetcher:
    def __init__(self):
        self.base_url = "https://www.shidianguji.com"
        self.book_id = "HY1523"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_chapter_list(self):
        """获取所有章节列表"""
        print("正在获取章节列表...")
        
        # 首先访问书籍主页获取章节列表
        book_url = f"{self.base_url}/book/{self.book_id}"
        try:
            response = self.session.get(book_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找章节链接
            chapter_links = []
            
            # 方法1: 查找章节导航
            nav_links = soup.find_all('a', href=re.compile(r'/chapter/'))
            for link in nav_links:
                href = link.get('href')
                if href and self.book_id in href:
                    chapter_links.append({
                        'url': urljoin(self.base_url, href),
                        'title': link.get_text(strip=True) or f"章节{len(chapter_links)+1}"
                    })
            
            # 方法2: 如果上面没找到，尝试API接口
            if not chapter_links:
                api_url = f"{self.base_url}/api/book/{self.book_id}/chapters"
                try:
                    api_response = self.session.get(api_url)
                    if api_response.status_code == 200:
                        data = api_response.json()
                        if 'chapters' in data:
                            for chapter in data['chapters']:
                                chapter_links.append({
                                    'url': urljoin(self.base_url, chapter.get('url', '')),
                                    'title': chapter.get('title', f"章节{len(chapter_links)+1}")
                                })
                except Exception as e:
                    print(f"API获取章节列表失败: {e}")
            
            # 方法3: 如果还是没找到，使用已知的章节模式
            if not chapter_links:
                # 根据搜索结果，我们知道有一些章节ID
                known_chapters = [
                    "1knwrejn2amuu",  # 小引
                    "1knwrejrl4zyj",  # 凡例
                    # 可以继续添加更多章节ID
                ]
                
                for i, chapter_id in enumerate(known_chapters):
                    chapter_links.append({
                        'url': f"{self.base_url}/book/{self.book_id}/chapter/{chapter_id}",
                        'title': f"章节{i+1}"
                    })
            
            print(f"找到 {len(chapter_links)} 个章节")
            return chapter_links
            
        except Exception as e:
            print(f"获取章节列表失败: {e}")
            return []
    
    def get_chapter_content(self, chapter_url, chapter_title):
        """获取单个章节的内容"""
        try:
            print(f"正在获取: {chapter_title}")
            response = self.session.get(chapter_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找主要内容区域
            content = ""
            
            # 方法1: 查找主要内容容器
            main_content = soup.find('div', class_=re.compile(r'content|text|chapter'))
            if main_content:
                content = main_content.get_text(separator='\n', strip=True)
            
            # 方法2: 如果上面没找到，查找所有文本内容
            if not content:
                # 移除脚本和样式标签
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # 获取body内容
                body = soup.find('body')
                if body:
                    content = body.get_text(separator='\n', strip=True)
            
            # 方法3: 如果还是没找到，获取整个页面文本
            if not content:
                content = soup.get_text(separator='\n', strip=True)
            
            # 清理内容
            content = self.clean_content(content)
            
            return content
            
        except Exception as e:
            print(f"获取章节内容失败 {chapter_title}: {e}")
            return ""
    
    def clean_content(self, content):
        """清理内容格式"""
        # 移除多余的空白行
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        # 重新组合，确保段落间有适当间距
        content = '\n\n'.join(cleaned_lines)
        
        # 移除常见的网页元素
        content = re.sub(r'识典古籍.*?版权所有', '', content, flags=re.DOTALL)
        content = re.sub(r'登录后阅读更方便', '', content)
        content = re.sub(r'书库', '', content)
        
        return content
    
    def save_to_markdown(self, chapters_data, filename="梦林玄解.md"):
        """保存为markdown文件"""
        print(f"正在保存到 {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            # 写入标题
            f.write("# 梦林玄解\n\n")
            f.write("**作者：** [北宋] 邵雍 纂辑 · [明] 陈士元 增删 · [明] 何栋如 重编\n\n")
            f.write("**来源：** 识典古籍 (https://www.shidianguji.com/)\n\n")
            f.write("---\n\n")
            
            # 写入目录
            f.write("## 目录\n\n")
            for i, chapter in enumerate(chapters_data, 1):
                f.write(f"{i}. [{chapter['title']}](#{chapter['title'].replace(' ', '-')})\n")
            f.write("\n---\n\n")
            
            # 写入各章节内容
            for i, chapter in enumerate(chapters_data, 1):
                f.write(f"## {i}. {chapter['title']}\n\n")
                f.write(f"**来源链接：** {chapter['url']}\n\n")
                f.write("---\n\n")
                f.write(chapter['content'])
                f.write("\n\n---\n\n")
        
        print(f"保存完成！共保存 {len(chapters_data)} 个章节")
    
    def fetch_all(self):
        """获取所有章节"""
        print("开始获取《梦林玄解》...")
        
        # 获取章节列表
        chapters = self.get_chapter_list()
        
        if not chapters:
            print("未找到任何章节，尝试使用已知章节...")
            # 使用已知的章节
            chapters = [
                {
                    'url': f"{self.base_url}/book/{self.book_id}/chapter/1knwrejn2amuu",
                    'title': "梦林玄解小引"
                },
                {
                    'url': f"{self.base_url}/book/{self.book_id}/chapter/1knwrejrl4zyj", 
                    'title': "梦林玄解凡例"
                }
            ]
        
        # 获取每个章节的内容
        chapters_data = []
        for i, chapter in enumerate(chapters, 1):
            print(f"进度: {i}/{len(chapters)}")
            content = self.get_chapter_content(chapter['url'], chapter['title'])
            
            if content:
                chapters_data.append({
                    'title': chapter['title'],
                    'url': chapter['url'],
                    'content': content
                })
            
            # 添加延迟避免请求过快
            time.sleep(1)
        
        # 保存为markdown文件
        if chapters_data:
            self.save_to_markdown(chapters_data)
        else:
            print("未获取到任何内容")

def main():
    fetcher = MenglinXuanjieFetcher()
    fetcher.fetch_all()

if __name__ == "__main__":
    main() 