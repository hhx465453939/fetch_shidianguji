#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试二级目录结构优化
"""

import os
import sys
import time
from fetch_book import ShidiangujiFetcher

def test_optimized_fetcher():
    """测试优化后的获取器"""
    print("测试优化后的识典古籍获取器")
    print("=" * 50)
    
    # 设置测试参数
    os.environ['BOOK_ID'] = 'DZ1040'
    os.environ['BOOK_TITLE'] = '皇极经世精校版'
    os.environ['OUTPUT_DIR'] = 'output'
    os.environ['REQUEST_DELAY'] = '1'
    
    # 创建获取器
    fetcher = ShidiangujiFetcher()
    
    print("\n1. 分析书籍结构...")
    start_time = time.time()
    chapters = fetcher.analyze_book_structure()
    analyze_time = time.time() - start_time
    
    print(f"\n分析完成！用时: {analyze_time:.2f} 秒")
    print(f"找到 {len(chapters)} 个章节")
    
    if chapters:
        print("\n前10个章节:")
        for i, chapter in enumerate(chapters[:10], 1):
            print(f"{i:2d}. {chapter['title']}")
        
        print(f"\n... 还有 {len(chapters) - 10} 个章节" if len(chapters) > 10 else "")
        
        # 测试内容获取
        print("\n2. 测试内容获取...")
        test_chapters = chapters[:3]  # 只测试前3个章节
        
        for chapter in test_chapters:
            print(f"\n测试章节: {chapter['title']}")
            content = fetcher.get_chapter_content(chapter['url'], chapter['title'])
            
            if content:
                print(f"  内容长度: {len(content)} 字符")
                print(f"  内容预览: {content[:100]}...")
            else:
                print("  未获取到有效内容")
            
            time.sleep(1)  # 延迟
    
    print("\n测试完成！")

def main():
    try:
        test_optimized_fetcher()
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()