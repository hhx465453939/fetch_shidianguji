#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容清理脚本
清理和优化获取的《梦林玄解》内容
"""

import re

def clean_content(content):
    """清理内容"""
    # 移除重复的章节标题
    lines = content.split('\n')
    cleaned_lines = []
    seen_titles = set()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是重复的章节标题
        if re.match(r'^梦林玄解.*$', line):
            if line in seen_titles:
                continue
            seen_titles.add(line)
        
        cleaned_lines.append(line)
    
    # 重新组合内容
    content = '\n\n'.join(cleaned_lines)
    
    # 移除其他重复内容
    content = re.sub(r'梦林玄解\n\n梦林玄解', '梦林玄解', content)
    content = re.sub(r'\[北宋\] 邵雍 纂辑.*?重编\n\n', '', content)
    
    # 移除导航链接
    content = re.sub(r'下一篇\n\n.*?\n\n', '', content, flags=re.DOTALL)
    
    return content

def main():
    # 读取原始文件
    input_file = '梦林玄解_智能获取_20250816_232815.md'
    output_file = '梦林玄解_清理版.md'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("正在清理内容...")
        
        # 分割章节
        sections = content.split('## ')
        
        # 处理每个章节
        cleaned_sections = []
        for i, section in enumerate(sections):
            if i == 0:  # 标题部分
                cleaned_sections.append(section)
                continue
                
            # 分离章节标题和内容
            lines = section.split('\n', 1)
            if len(lines) < 2:
                continue
                
            title = lines[0]
            chapter_content = lines[1] if len(lines) > 1 else ""
            
            # 清理章节内容
            cleaned_content = clean_content(chapter_content)
            
            # 重新组合
            cleaned_section = f"## {title}\n\n{cleaned_content}"
            cleaned_sections.append(cleaned_section)
        
        # 重新组合整个文档
        cleaned_content = '\n\n'.join(cleaned_sections)
        
        # 保存清理后的文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"清理完成！保存到 {output_file}")
        
    except Exception as e:
        print(f"清理失败: {e}")

if __name__ == "__main__":
    main() 