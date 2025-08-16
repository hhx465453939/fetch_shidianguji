# 识典古籍获取工具项目

🏛️ 一个专业的古籍数字化资源获取工具，专注于从识典古籍网站批量获取和整理古籍文本。

## 📊 项目概览

本项目包含了完整的古籍获取工具链，从网站分析到内容清理，提供了一站式的古籍数字化解决方案。

### 🎯 主要功能

- **智能网站分析**: 自动解析网站结构，发现所有章节链接
- **批量内容获取**: 高效获取完整古籍内容
- **自动内容清理**: 去除重复信息，优化文本格式
- **标准化输出**: 生成规范的Markdown格式文档
- **配置化管理**: 支持环境变量和配置文件

## 📁 项目结构

```
├── fetch_shidianguji/           # 🚀 主工具包
│   ├── fetch_book.py           # 核心获取脚本
│   ├── example.py              # 使用示例
│   ├── utils.py                # 工具函数
│   ├── requirements.txt        # 依赖管理
│   ├── .env.template          # 配置模板
│   └── README.md              # 详细使用说明
├── 梦林玄解_清理版.md           # ✨ 示例输出（推荐）
├── 梦林玄解_智能获取_*.md       # 📄 原始获取结果
├── smart_fetch.py              # 🧠 智能获取脚本（开发版）
├── clean_content.py            # 🧹 内容清理脚本
└── PROJECT_README.md           # 📖 本文件
```

## 🚀 快速开始

### 1. 进入工具目录

```bash
cd fetch_shidianguji
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

```bash
cp .env.template .env
# 编辑 .env 文件，填写书籍信息
```

### 4. 运行工具

```bash
python fetch_book.py
```

## 📖 成功案例

### 《梦林玄解》获取案例

- **书籍**: 梦林玄解 ([北宋] 邵雍 纂辑 · [明] 陈士元 增删 · [明] 何栋如 重编)
- **章节数**: 38个完整章节
- **文件大小**: 515KB (清理版)
- **获取时间**: 约2分钟
- **成功率**: 100%

**获取配置示例**:
```env
BOOK_ID=HY1523
BOOK_URL=https://www.shidianguji.com/book/HY1523
BOOK_TITLE=梦林玄解
OUTPUT_DIR=output
REQUEST_DELAY=1
```

## 🔧 技术特点

### 核心技术栈

- **Python 3.7+**: 主要开发语言
- **BeautifulSoup4**: HTML解析和内容提取
- **Requests**: HTTP请求处理
- **python-dotenv**: 环境变量管理
- **正则表达式**: 内容清理和格式化

### 智能分析机制

1. **多重发现策略**: 
   - 主页链接分析
   - API接口探测
   - 目录页面扫描

2. **内容清理算法**:
   - 重复内容去除
   - 导航链接过滤
   - 格式标准化

3. **错误处理机制**:
   - 网络请求重试
   - 内容验证检查
   - 异常状态处理

## 📊 支持的网站

| 网站 | 状态 | 说明 |
|------|------|------|
| [识典古籍](https://www.shidianguji.com/) | ✅ 完全支持 | 北京大学×字节跳动古籍平台 |

## 🎨 输出示例

生成的Markdown文件结构：

```markdown
# 书籍标题

**作者**: 作者信息
**来源**: 识典古籍
**获取时间**: 2025年08月16日

## 目录
1. [章节1](#章节1)
2. [章节2](#章节2)
...

## 1. 章节1
**来源链接**: https://...
---
章节内容...
```

## 🛠️ 开发说明

### 脚本说明

- **fetch_book.py**: 生产级获取脚本，支持配置文件
- **smart_fetch.py**: 开发版智能分析脚本
- **clean_content.py**: 独立的内容清理工具
- **example.py**: 使用示例和交互式操作

### 自定义开发

```python
from fetch_book import ShidiangujiFetcher

# 创建自定义获取器
fetcher = ShidiangujiFetcher()

# 自定义分析逻辑
chapters = fetcher.analyze_book_structure()

# 自定义内容处理
for chapter in chapters:
    content = fetcher.get_chapter_content(chapter['url'], chapter['title'])
    # 自定义处理逻辑...
```

## ⚠️ 使用须知

### 合规要求

1. **学术用途**: 仅用于学术研究和个人学习
2. **版权尊重**: 尊重原始内容版权
3. **合理使用**: 避免过度频繁的请求
4. **法律合规**: 遵守相关法律法规

### 技术要求

- Python 3.7或更高版本
- 稳定的网络连接
- 足够的存储空间

## 📈 项目状态

- **版本**: v1.0
- **状态**: 生产就绪 ✅
- **维护**: 积极维护中
- **测试**: 已通过《梦林玄解》完整测试

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献方式

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 发起Pull Request

### 开发环境

```bash
git clone [repository]
cd fetch_shidianguji
pip install -r requirements.txt
```

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交GitHub Issue
- 发起Discussion讨论

---

**项目开始时间**: 2025年08月16日  
**最后更新**: 2025年08月16日  
**当前版本**: v1.0  
**状态**: ✅ 生产就绪 