#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例脚本
演示如何使用识典古籍获取脚本
"""

import os
import sys
from fetch_book import ShidiangujiFetcher

def example_menglin():
    """示例：获取《梦林玄解》"""
    print("示例：获取《梦林玄解》")
    
    # 设置环境变量
    os.environ['BOOK_ID'] = 'HY1523'
    os.environ['BOOK_TITLE'] = '梦林玄解'
    os.environ['OUTPUT_DIR'] = 'output'
    os.environ['REQUEST_DELAY'] = '2'
    
    # 创建获取器
    fetcher = ShidiangujiFetcher()
    
    # 获取书籍
    result = fetcher.fetch_book('梦林玄解')
    
    if result:
        print(f"✅ 获取完成！文件保存在: {result}")
    else:
        print("❌ 获取失败")

def example_from_url():
    """示例：从URL获取书籍"""
    print("示例：从URL获取书籍")
    
    # 可以使用任何识典古籍的书籍URL
    book_url = input("请输入书籍URL (例如: https://www.shidianguji.com/book/HY1523): ")
    book_title = input("请输入书籍标题 (可选): ")
    
    if not book_url:
        print("❌ 未提供书籍URL")
        return
    
    # 设置环境变量
    os.environ['BOOK_URL'] = book_url
    if book_title:
        os.environ['BOOK_TITLE'] = book_title
    os.environ['OUTPUT_DIR'] = 'output'
    os.environ['REQUEST_DELAY'] = '1'
    
    # 创建获取器
    fetcher = ShidiangujiFetcher()
    
    # 获取书籍
    result = fetcher.fetch_book(book_title or None)
    
    if result:
        print(f"✅ 获取完成！文件保存在: {result}")
    else:
        print("❌ 获取失败")

def main():
    print("识典古籍获取脚本 - 使用示例")
    print("=" * 40)
    print("1. 获取《梦林玄解》(示例)")
    print("2. 从URL获取书籍")
    print("3. 退出")
    
    choice = input("请选择 (1-3): ")
    
    if choice == '1':
        example_menglin()
    elif choice == '2':
        example_from_url()
    elif choice == '3':
        print("退出")
        sys.exit(0)
    else:
        print("无效选择")

if __name__ == "__main__":
    main() 