# 识典古籍获取工具

一个用于从识典古籍网站 (https://www.shidianguji.com/) 批量获取古籍文本的Python工具。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

复制配置模板并填写配置：

```bash
cp .env.template .env
```

编辑 `.env` 文件，填写书籍信息：

```env
# 书籍ID（从书籍URL中提取）
BOOK_ID=HY1523

# 或者直接提供完整的书籍URL
BOOK_URL=https://www.shidianguji.com/book/HY1523

# 书籍标题（可选）
BOOK_TITLE=梦林玄解

# 输出目录（可选，默认为 output）
OUTPUT_DIR=output

# 请求延迟（秒，默认为1秒）
REQUEST_DELAY=1
```

**获取配置示例**:
```env
BOOK_ID=HY1523
BOOK_URL=https://www.shidianguji.com/book/HY1523
BOOK_TITLE=梦林玄解
OUTPUT_DIR=output
REQUEST_DELAY=1
```

### 3. 运行获取脚本

```bash
python fetch_book.py
```

或运行示例：

```bash
python example.py
```

## 📁 项目结构

```
fetch_shidianguji/
├── fetch_book.py      # 主获取脚本
├── example.py         # 使用示例
├── utils.py          # 工具函数
├── requirements.txt   # 依赖文件
├── .env.template     # 配置模板
├── README.md         # 项目说明
└── output/           # 输出目录（自动创建）
```

## 🔧 功能特点

- **智能分析**: 自动分析网站结构，发现所有章节
- **批量获取**: 一次性获取整本书的所有章节
- **内容清理**: 自动去除重复内容和无关信息
- **格式优化**: 生成规范的markdown格式
- **错误处理**: 完整的错误处理和重试机制
- **配置灵活**: 支持环境变量配置

## 📖 使用方法

### 方法1: 使用书籍ID

1. 从书籍URL中提取ID，例如：
   `https://www.shidianguji.com/book/HY1523` → `HY1523`

2. 在 `.env` 文件中设置：
   ```env
   BOOK_ID=HY1523
   BOOK_TITLE=梦林玄解
   ```

### 方法2: 使用完整URL

直接在 `.env` 文件中设置完整URL：
```env
BOOK_URL=https://www.shidianguji.com/book/HY1523
BOOK_TITLE=梦林玄解
```

### 方法3: 编程调用

```python
import os
from fetch_book import ShidiangujiFetcher

# 设置环境变量
os.environ['BOOK_ID'] = 'HY1523'
os.environ['BOOK_TITLE'] = '梦林玄解'

# 创建获取器并运行
fetcher = ShidiangujiFetcher()
result = fetcher.fetch_book('梦林玄解')

if result:
    print(f"获取完成！文件保存在: {result}")
```

## ⚙️ 配置选项

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| BOOK_ID | 书籍ID | - | HY1523 |
| BOOK_URL | 完整书籍URL | - | https://www.shidianguji.com/book/HY1523 |
| BOOK_TITLE | 书籍标题 | - | 梦林玄解 |
| OUTPUT_DIR | 输出目录 | output | output |
| REQUEST_DELAY | 请求延迟(秒) | 1 | 1 |

## 📋 输出格式

生成的markdown文件包含：

- 书籍标题和作者信息
- 获取时间和方式
- 完整的章节目录
- 各章节的详细内容
- 原始链接信息

## 🛠️ 技术实现

- **网页解析**: 使用 BeautifulSoup 解析HTML
- **HTTP请求**: 使用 requests 库处理网络请求
- **配置管理**: 使用 python-dotenv 管理环境变量
- **内容清理**: 正则表达式清理和格式化
- **错误处理**: 完整的异常处理和重试机制

## ⚠️ 注意事项

1. **合规使用**: 仅用于学术研究和个人学习
2. **请求频率**: 默认每次请求间隔1秒，避免过于频繁
3. **网络环境**: 需要稳定的网络连接
4. **存储空间**: 确保有足够的磁盘空间存储文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具。

## 📄 许可证

本项目仅用于学术研究和学习目的，请遵守相关法律法规和网站使用条款。

## 📊 支持的网站

- [识典古籍](https://www.shidianguji.com/) - 北京大学与字节跳动联合开发的古籍数字化平台

---

**最后更新**: 2025年08月16日 