#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能版《梦林玄解》获取脚本
分析网站结构并获取所有章节
"""

import requests
import time
from bs4 import BeautifulSoup
import re
import json

def analyze_book_structure(book_id):
    """分析书籍结构，尝试获取所有章节信息"""
    print("正在分析书籍结构...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 尝试访问书籍主页
    book_url = f"https://www.shidianguji.com/book/{book_id}"
    
    try:
        response = requests.get(book_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找章节链接
        chapter_links = []
        
        # 方法1: 查找所有包含chapter的链接
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href')
            if '/chapter/' in href and book_id in href:
                title = link.get_text(strip=True)
                if title:
                    chapter_links.append({
                        'url': f"https://www.shidianguji.com{href}",
                        'title': title
                    })
        
        # 方法2: 尝试API接口
        api_url = f"https://www.shidianguji.com/api/book/{book_id}/chapters"
        try:
            api_response = requests.get(api_url, headers=headers)
            if api_response.status_code == 200:
                data = api_response.json()
                print(f"API返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"API请求失败: {e}")
        
        # 方法3: 尝试获取目录页面
        toc_url = f"https://www.shidianguji.com/book/{book_id}/toc"
        try:
            toc_response = requests.get(toc_url, headers=headers)
            if toc_response.status_code == 200:
                toc_soup = BeautifulSoup(toc_response.content, 'html.parser')
                toc_links = toc_soup.find_all('a', href=True)
                for link in toc_links:
                    href = link.get('href')
                    if '/chapter/' in href:
                        title = link.get_text(strip=True)
                        if title:
                            chapter_links.append({
                                'url': f"https://www.shidianguji.com{href}",
                                'title': title
                            })
        except Exception as e:
            print(f"目录页面请求失败: {e}")
        
        print(f"找到 {len(chapter_links)} 个章节链接")
        return chapter_links
        
    except Exception as e:
        print(f"分析书籍结构失败: {e}")
        return []

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

def generate_chapter_urls(book_id):
    """基于已知模式生成可能的章节URL"""
    print("正在生成可能的章节URL...")
    
    # 已知的章节ID模式
    known_ids = [
        "1knwrejn2amuu",  # 小引
        "1knwrejrl4zyj",  # 凡例
    ]
    
    # 尝试生成更多可能的ID
    # 基于已知ID的模式，尝试生成其他章节
    base_patterns = [
        "1knwrejn",  # 小引的基础模式
        "1knwrejrl",  # 凡例的基础模式
    ]
    
    generated_urls = []
    
    # 添加已知的章节
    for chapter_id in known_ids:
        generated_urls.append({
            'url': f"https://www.shidianguji.com/book/{book_id}/chapter/{chapter_id}",
            'title': f"章节_{chapter_id}"
        })
    
    # 尝试生成更多可能的ID
    for base in base_patterns:
        for i in range(1, 50):  # 尝试1-50
            # 尝试不同的后缀模式
            suffixes = [
                f"{i:02d}",
                f"{i:03d}",
                f"a{i:02d}",
                f"b{i:02d}",
                f"c{i:02d}",
            ]
            
            for suffix in suffixes:
                chapter_id = f"{base}{suffix}"
                generated_urls.append({
                    'url': f"https://www.shidianguji.com/book/{book_id}/chapter/{chapter_id}",
                    'title': f"章节_{chapter_id}"
                })
    
    print(f"生成了 {len(generated_urls)} 个可能的URL")
    return generated_urls

def main():
    book_id = "HY1523"
    
    # 方法1: 分析网站结构
    chapters = analyze_book_structure(book_id)
    
    # 方法2: 如果分析失败，使用已知章节
    if not chapters:
        print("网站结构分析失败，使用已知章节...")
        chapters = [
            {'url': 'https://www.shidianguji.com/book/HY1523/chapter/1knwrejn2amuu', 'title': '梦林玄解小引'},
            {'url': 'https://www.shidianguji.com/book/HY1523/chapter/1knwrejrl4zyj', 'title': '梦林玄解凡例'},
        ]
    
    # 方法3: 生成可能的章节URL
    if len(chapters) < 5:  # 如果找到的章节太少，尝试生成更多
        print("找到的章节较少，尝试生成更多可能的URL...")
        generated_chapters = generate_chapter_urls(book_id)
        chapters.extend(generated_chapters)
    
    # 去重
    seen_urls = set()
    unique_chapters = []
    for chapter in chapters:
        if chapter['url'] not in seen_urls:
            seen_urls.add(chapter['url'])
            unique_chapters.append(chapter)
    
    print(f"准备获取 {len(unique_chapters)} 个章节...")
    
    # 获取内容
    all_content = []
    for i, chapter in enumerate(unique_chapters, 1):
        print(f"进度: {i}/{len(unique_chapters)}")
        content = get_chapter_content(chapter['url'], chapter['title'])
        if content and len(content) > 100:  # 只保存有实际内容的章节
            all_content.append({
                'title': chapter['title'],
                'url': chapter['url'],
                'content': content
            })
        time.sleep(1)  # 避免请求过快
    
    # 保存为markdown
    if all_content:
        filename = f'梦林玄解_智能获取_{time.strftime("%Y%m%d_%H%M%S")}.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 梦林玄解\n\n")
            f.write("**作者：** [北宋] 邵雍 纂辑 · [明] 陈士元 增删 · [明] 何栋如 重编\n\n")
            f.write("**来源：** 识典古籍 (https://www.shidianguji.com/)\n\n")
            f.write("**获取时间：** " + time.strftime("%Y年%m月%d日 %H:%M:%S") + "\n\n")
            f.write("**获取方式：** 智能分析网站结构\n\n")
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
        
        print(f"保存完成！共保存 {len(all_content)} 个章节到 {filename}")
    else:
        print("未获取到任何内容")

if __name__ == "__main__":
    main() 