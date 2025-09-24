# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个用于从识典古籍网站 (https://www.shidianguji.com/) 批量获取古籍文本的Python工具。该工具通过智能分析网站结构，自动发现所有章节并批量获取内容，最终生成规范的markdown格式文件。

## 核心架构

### 主要组件

1. **ShidiangujiFetcher类** (`fetch_book.py`)
   - 核心获取引擎，负责整个获取流程
   - 支持多种章节发现策略：直接链接解析、API接口、目录页面
   - 内置内容清理和格式化功能
   - 自动生成带目录的markdown文件

2. **工具函数库** (`utils.py`)
   - URL解析和ID提取
   - 文件名清理和格式化
   - 进度显示和计时器
   - 目录创建和安全睡眠

### 配置系统

使用 `.env` 文件进行配置，支持两种模式：
- **BOOK_ID模式**: 直接使用书籍ID（推荐）
- **BOOK_URL模式**: 使用完整的书籍URL

### 数据流

1. 从.env加载配置 → 2. 分析书籍结构发现章节 → 3. 批量获取章节内容 → 4. 清理和去重 → 5. 生成markdown文件

## 常用命令

### 开发环境设置
```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python fetch_book.py

# 运行示例程序
python example.py
```

### 测试和调试
```bash
# 测试特定书籍ID
export BOOK_ID=HY1523
export BOOK_TITLE=测试书籍
python fetch_book.py
```

## 开发注意事项

### 网站结构变化处理
- 当前工具支持多种章节发现策略来应对网站结构变化
- 在`analyze_book_structure()`中添加了三种不同的发现方法
- 如果网站结构发生变化，优先检查前两种方法，必要时添加新的发现策略

### 请求频率控制
- 默认请求间隔为1秒，可在.env中通过`REQUEST_DELAY`调整
- 使用`session`对象保持连接，提高效率
- 内置错误处理和重试机制

### 内容清理规则
- 移除脚本、样式和导航元素
- 去除版权信息和重复标题
- 使用正则表达式清理多余空白和重复内容
- 保留原文格式结构

### 输出格式规范
- 文件名格式：`{书名}_{时间戳}.md`
- 包含完整的目录结构
- 每章包含来源链接和内容分隔线
- 元数据包含获取时间、来源和方式信息

## 扩展开发

### 添加新的数据源
1. 创建新的Fetcher类继承基础模式
2. 实现特定的网站解析逻辑
3. 更新配置系统支持新参数

### 改进内容清理
- 在`clean_content()`方法中添加新的清理规则
- 使用更精细的正则表达式或NLP技术
- 保留古籍特有的格式标记

### 性能优化
- 实现并发请求（注意网站限制）
- 添加缓存机制避免重复获取
- 优化内存使用处理大型古籍