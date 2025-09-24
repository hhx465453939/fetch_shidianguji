#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
识典古籍通用获取脚本
支持从.env文件读取配置，批量获取古籍内容
"""

import requests
import time
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from dotenv import load_dotenv

class ShidiangujiFetcher:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        self.base_url = "https://www.shidianguji.com"
        self.book_id = os.getenv('BOOK_ID', '')
        self.book_url = os.getenv('BOOK_URL', '')
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.delay = int(os.getenv('REQUEST_DELAY', '1'))
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
    def extract_book_id_from_url(self, url):
        """从URL中提取书籍ID"""
        if not url:
            return None
            
        # 匹配 /book/HY1523/ 这样的模式
        match = re.search(r'/book/([^/]+)/', url)
        if match:
            return match.group(1)
        return None
    
    def analyze_book_structure(self):
        """分析书籍结构，获取所有章节信息"""
        print("正在分析书籍结构...")
        
        if not self.book_id and self.book_url:
            self.book_id = self.extract_book_id_from_url(self.book_url)
        
        if not self.book_id:
            print("错误：未提供书籍ID或有效的书籍URL")
            return []
        
        # 尝试访问书籍主页
        book_url = f"{self.base_url}/book/{self.book_id}"
        
        try:
            response = self.session.get(book_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找章节链接
            chapter_links = []
            
            # 方法1: 查找所有包含chapter的链接（支持多级目录）
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                if '/chapter/' in href and self.book_id in href:
                    title = link.get_text(strip=True)
                    if title and len(title) > 1:  # 过滤掉空标题或单字符
                        chapter_links.append({
                            'url': f"{self.base_url}{href}",
                            'title': title
                        })
            
            # 方法2: 尝试API接口
            api_url = f"{self.base_url}/api/book/{self.book_id}/chapters"
            try:
                api_response = self.session.get(api_url)
                if api_response.status_code == 200:
                    data = api_response.json()
                    print(f"API返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                    # 从API数据中提取章节
                    if 'chapters' in data:
                        for chapter in data['chapters']:
                            chapter_links.append({
                                'url': f"{self.base_url}/book/{self.book_id}/chapter/{chapter['id']}",
                                'title': chapter.get('title', f'章节{chapter["id"]}')
                            })
            except Exception as e:
                print(f"API请求失败: {e}")
            
            # 方法3: 尝试获取目录页面
            toc_url = f"{self.base_url}/book/{self.book_id}/toc"
            try:
                toc_response = self.session.get(toc_url)
                if toc_response.status_code == 200:
                    toc_soup = BeautifulSoup(toc_response.content, 'html.parser')
                    # 查找可能包含章节的容器
                    chapter_containers = toc_soup.find_all(['div', 'nav', 'ul'], class_=lambda x: x and ('chapter' in x or 'toc' in x or 'menu' in x))
                    
                    for container in chapter_containers:
                        links = container.find_all('a', href=True)
                        for link in links:
                            href = link.get('href')
                            if '/chapter/' in href and self.book_id in href:
                                title = link.get_text(strip=True)
                                if title and len(title) > 1:
                                    chapter_links.append({
                                        'url': f"{self.base_url}{href}",
                                        'title': title
                                    })
            except Exception as e:
                print(f"目录页面请求失败: {e}")
            
            # 方法4: 尝试从章节页面发现二级目录结构
            print("尝试发现二级目录结构...")
            enhanced_chapters = self._discover_nested_chapters(chapter_links)
            if enhanced_chapters:
                chapter_links = enhanced_chapters
            
            # 去重
            seen_urls = set()
            unique_chapters = []
            for chapter in chapter_links:
                if chapter['url'] not in seen_urls:
                    seen_urls.add(chapter['url'])
                    unique_chapters.append(chapter)
            
            print(f"找到 {len(unique_chapters)} 个章节链接")
            return unique_chapters
            
        except Exception as e:
            print(f"分析书籍结构失败: {e}")
            return []
    
    def _discover_nested_chapters(self, initial_chapters):
        """发现二级目录结构"""
        nested_chapters = []
        seen_titles = set()
        
        # 基于对网站结构的分析，直接从主页面获取所有章节链接
        print("从主页面获取完整章节列表...")
        
        try:
            # 访问书籍主页
            book_url = f"{self.base_url}/book/{self.book_id}"
            response = self.session.get(book_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找所有章节链接
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                if '/chapter/' in href and self.book_id in href:
                    title = link.get_text(strip=True)
                    # 过滤有效的章节标题
                    if (title and len(title) > 2 and  # 至少3个字符
                        title not in seen_titles and
                        title not in ['下一篇', '上一章', '目录', '返回', '书库'] and
                        ('皇极经世' in title or '发音' in title or '收音' in title or '闭音' in title)):
                        nested_chapters.append({
                            'url': f"{self.base_url}{href}",
                            'title': title
                        })
                        seen_titles.add(title)
                        print(f"  发现章节: {title}")
            
            print(f"从主页共发现 {len(nested_chapters)} 个章节")
            
        except Exception as e:
            print(f"从主页获取章节失败: {e}")
            # 如果主页失败，回到原来的方法
            return self._discover_chapters_from_samples(initial_chapters)
        
        # 使用发现的完整章节列表替换初始章节
        return nested_chapters
    
    def _discover_chapters_from_samples(self, initial_chapters):
        """从样本章节中发现二级目录结构（备用方法）"""
        nested_chapters = []
        seen_titles = set()
        
        # 只取前几个章节进行分析，避免请求过多
        sample_size = min(3, len(initial_chapters))
        print(f"分析前 {sample_size} 个章节以发现二级结构...")
        
        for i, chapter in enumerate(initial_chapters[:sample_size]):
            print(f"分析章节 {i+1}/{sample_size}: {chapter['title']}")
            
            try:
                # 检查章节页面是否包含二级目录
                response = self.session.get(chapter['url'])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 查找页面中的侧边栏导航（基于实际HTML结构）
                sidebar_elements = soup.find_all(['aside', 'nav', 'div'], 
                    class_=lambda x: x and any(keyword in x.lower() for keyword in 
                    ['sidebar', 'nav', 'menu', 'chapter', '目录', '导航']))
                
                # 在章节页面中查找额外的链接
                for sidebar in sidebar_elements:
                    links = sidebar.find_all('a', href=True)
                    for link in links:
                        href = link.get('href')
                        if '/chapter/' in href and self.book_id in href and href != chapter['url']:
                            title = link.get_text(strip=True)
                            # 更严格的标题过滤
                            if (title and len(title) > 2 and 
                                title not in seen_titles and
                                title not in ['下一篇', '上一章', '目录', '返回', '书库'] and
                                ('皇极经世' in title or '发音' in title or '收音' in title or '闭音' in title)):
                                nested_chapters.append({
                                    'url': f"{self.base_url}{href}",
                                    'title': title
                                })
                                seen_titles.add(title)
                                print(f"  发现二级章节: {title}")
                
                # 添加延迟
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"分析章节 {chapter['title']} 失败: {e}")
                continue
        
        # 合并初始章节和发现的二级章节，但去重
        all_chapters = []
        seen_urls = set()
        
        # 先添加初始章节
        for chapter in initial_chapters:
            if chapter['url'] not in seen_urls:
                all_chapters.append(chapter)
                seen_urls.add(chapter['url'])
        
        # 添加新的章节（避免重复）
        for chapter in nested_chapters:
            if chapter['url'] not in seen_urls:
                all_chapters.append(chapter)
                seen_urls.add(chapter['url'])
        
        print(f"去重后共发现 {len(all_chapters)} 个章节")
        return all_chapters
    
    def get_chapter_content(self, url, title):
        """获取章节内容"""
        print(f"正在获取: {title}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除脚本和样式
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 基于实际页面结构，优先查找article元素
            article_content = soup.find('article')
            if article_content:
                content = article_content.get_text(separator='\n', strip=True)
            else:
                # 查找主要内容区域
                content_selectors = [
                    '.chapter-reader-content',
                    '.content',
                    '.main-content',
                    '.text-content',
                    '#content',
                    '[class*="content"]',
                    '[class*="text"]',
                    '[class*="chapter"]'
                ]
                
                content_elements = []
                for selector in content_selectors:
                    elements = soup.select(selector)
                    content_elements.extend(elements)
                
                # 如果没有找到特定内容区域，使用主要文本内容
                if not content_elements:
                    # 移除导航、页眉、页脚等
                    for unwanted in soup.find_all(['nav', 'header', 'footer', 'aside', '.nav', '.menu', '.sidebar']):
                        unwanted.decompose()
                    
                    content = soup.get_text(separator='\n', strip=True)
                else:
                    # 使用找到的最大内容元素
                    main_content = max(content_elements, key=lambda x: len(x.get_text()))
                    content = main_content.get_text(separator='\n', strip=True)
            
            # 检查内容长度，对于皇极经世来说，短内容是正常的
            if len(content.strip()) < 10:
                print(f"  警告: {title} 内容为空")
                return ""
            
            # 清理内容
            content = re.sub(r'识典古籍.*?版权所有', '', content, flags=re.DOTALL)
            content = re.sub(r'登录后阅读更方便', '', content)
            content = re.sub(r'书库', '', content)
            content = re.sub(r'下一篇.*?$', '', content, flags=re.MULTILINE)
            content = re.sub(r'上一章.*?$', '', content, flags=re.MULTILINE)
            content = re.sub(r'目录', '', content)
            
            # 移除多余的空白行
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n\n'.join(lines)
            
            return content
            
        except Exception as e:
            print(f"获取失败: {e}")
            return ""
    
    def clean_content(self, content):
        """清理内容格式"""
        # 移除重复的章节标题
        lines = content.split('\n')
        cleaned_lines = []
        seen_titles = set()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是重复的章节标题（常见的古籍标题模式）
            title_patterns = [
                r'^.*卷.*[上下中]$',
                r'^.*卷.*第.*$',
                r'^.*章.*$',
                r'^.*节.*$',
                r'^.*篇.*$',
                r'^.*之.*$',
                r'^.*解.*$',
                r'^.*经.*$',
                r'^.*论.*$'
            ]
            
            is_title = False
            for pattern in title_patterns:
                if re.match(pattern, line):
                    is_title = True
                    break
            
            if is_title:
                if line in seen_titles:
                    continue
                seen_titles.add(line)
            
            cleaned_lines.append(line)
        
        # 重新组合内容
        content = '\n\n'.join(cleaned_lines)
        
        # 移除其他重复内容（基于常见的重复模式）
        content = re.sub(r'(.+)\s*\1+', r'\1', content)  # 移除完全重复的行
        
        # 清理常见的无关内容
        content = re.sub(r'识典古籍.*?版权所有', '', content, flags=re.DOTALL)
        content = re.sub(r'获取时间.*?获取方式', '', content, flags=re.DOTALL)
        content = re.sub(r'来源链接.*?$', '', content, flags=re.MULTILINE)
        
        # 移除空行过多的地方
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        return content
    
    def save_to_markdown(self, chapters_data, book_title="古籍"):
        """保存为markdown文件"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{book_title}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        print(f"正在保存到 {filepath}...")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # 写入标题
            f.write(f"# {book_title}\n\n")
            f.write("**来源：** 识典古籍 (https://www.shidianguji.com/)\n\n")
            f.write("**获取时间：** " + time.strftime("%Y年%m月%d日 %H:%M:%S") + "\n\n")
            f.write("**获取方式：** 智能分析网站结构\n\n")
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
        
        print(f"保存完成！共保存 {len(chapters_data)} 个章节到 {filepath}")
        return filepath
    
    def fetch_book(self, book_title=None):
        """获取整本书的内容"""
        print(f"开始获取书籍: {book_title or self.book_id}")
        
        # 获取章节列表
        chapters = self.analyze_book_structure()
        
        if not chapters:
            print("未找到任何章节")
            return None
        
        # 去重
        seen_urls = set()
        unique_chapters = []
        for chapter in chapters:
            if chapter['url'] not in seen_urls:
                seen_urls.add(chapter['url'])
                unique_chapters.append(chapter)
        
        print(f"准备获取 {len(unique_chapters)} 个章节...")
        
        # 获取每个章节的内容
        chapters_data = []
        for i, chapter in enumerate(unique_chapters, 1):
            print(f"进度: {i}/{len(unique_chapters)}")
            content = self.get_chapter_content(chapter['url'], chapter['title'])
            
            if content and len(content) > 100:  # 只保存有实际内容的章节
                cleaned_content = self.clean_content(content)
                chapters_data.append({
                    'title': chapter['title'],
                    'url': chapter['url'],
                    'content': cleaned_content
                })
            
            # 添加延迟避免请求过快
            time.sleep(self.delay)
        
        # 保存为markdown文件
        if chapters_data:
            return self.save_to_markdown(chapters_data, book_title or f"书籍_{self.book_id}")
        else:
            print("未获取到任何内容")
            return None

def main():
    fetcher = ShidiangujiFetcher()
    
    # 检查配置
    if not fetcher.book_id and not fetcher.book_url:
        print("错误：请在.env文件中配置BOOK_ID或BOOK_URL")
        print("示例：")
        print("BOOK_ID=HY1523")
        print("BOOK_URL=https://www.shidianguji.com/book/HY1523")
        return
    
    # 获取书籍标题
    book_title = os.getenv('BOOK_TITLE', None)
    
    # 开始获取
    result = fetcher.fetch_book(book_title)
    
    if result:
        print(f"✅ 获取完成！文件保存在: {result}")
    else:
        print("❌ 获取失败")

if __name__ == "__main__":
    main()