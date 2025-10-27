# 古籍MCP服务器 (Guji MCP Server)

## 项目概述

古籍MCP服务器是一个基于Model Context Protocol (MCP) 的智能古籍检索服务，专门为AI对话系统提供古籍知识支持。通过整合识典古籍网站的搜索功能，为AI助手提供实时的古籍文献检索和内容提取能力。

## 核心功能

### 🔍 智能搜索
- **关键词搜索**: 支持单关键词、多关键词、模糊搜索
- **分类筛选**: 按四部分类（经史子集）、朝代、作者筛选
- **内容类型**: 支持全文搜索、标题搜索、作者搜索
- **排序方式**: 相关度排序、朝代排序

### 📚 内容提取
- **书籍信息**: 书名、作者、朝代、版本信息
- **内容片段**: 包含关键词的原文段落
- **来源标注**: 完整的文献来源信息
- **质量标识**: 精校、粗校等版本质量信息

### 🤖 AI集成
- **MCP协议**: 标准化的AI助手接口
- **上下文增强**: 为对话提供古籍知识背景
- **智能引用**: 自动生成规范的文献引用
- **知识图谱**: 构建古籍知识关联网络

## 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI 助手      │    │   MCP 服务器    │    │  识典古籍网站   │
│  (Claude等)     │◄──►│  (本服务)       │◄──►│  (数据源)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   本地缓存      │
                       │  (Redis/SQLite) │
                       └─────────────────┘
```

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境
```bash
cp .env.template .env
# 编辑 .env 文件配置参数
```

### 启动服务
```bash
python -m guji_mcp_server
```

### 连接AI助手
```python
# 在AI助手中配置MCP服务器
{
  "mcpServers": {
    "guji-server": {
      "command": "python",
      "args": ["-m", "guji_mcp_server"],
      "cwd": "/path/to/guji-mcp-server"
    }
  }
}
```

## API接口

### 搜索接口
```python
# 基础搜索
search_ancient_texts(
    keyword: str,
    search_type: str = "full_text",  # full_text, title, author
    category: str = None,            # 四部分类
    dynasty: str = None,             # 朝代
    fuzzy: bool = True,              # 模糊搜索
    limit: int = 10                  # 结果数量
)

# 高级搜索
advanced_search(
    query: dict,                     # 复杂查询条件
    filters: dict = None,           # 过滤条件
    sort_by: str = "relevance"      # 排序方式
)
```

### 内容提取接口
```python
# 提取书籍信息
extract_book_info(book_id: str)

# 提取内容片段
extract_content_snippets(
    book_id: str,
    keyword: str,
    context_length: int = 200
)

# 获取完整章节
get_chapter_content(
    book_id: str,
    chapter_id: str
)
```

## 使用示例

### 基础搜索
```python
# 搜索包含"道"的古籍内容
results = search_ancient_texts("道", limit=5)

for result in results:
    print(f"书名: {result['title']}")
    print(f"作者: {result['author']}")
    print(f"朝代: {result['dynasty']}")
    print(f"内容: {result['snippet']}")
    print(f"来源: {result['source']}")
    print("---")
```

### 分类搜索
```python
# 在经部中搜索"易"相关内容
results = search_ancient_texts(
    keyword="易",
    category="经部",
    dynasty="先秦",
    limit=3
)
```

### 内容提取
```python
# 获取特定书籍的详细信息
book_info = extract_book_info("HY1523")
chapters = get_book_chapters("HY1523")

# 提取包含关键词的内容片段
snippets = extract_content_snippets(
    book_id="HY1523",
    keyword="皇极经世",
    context_length=300
)
```

## 配置说明

### 环境变量
```env
# 服务器配置
SERVER_HOST=localhost
SERVER_PORT=8000
DEBUG=False

# 缓存配置
CACHE_TYPE=redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# 搜索配置
DEFAULT_SEARCH_LIMIT=10
MAX_SEARCH_LIMIT=100
REQUEST_DELAY=1.0

# 内容过滤
MIN_CONTENT_LENGTH=50
FILTER_MODERN_CONTENT=True
```

## 开发指南

### 项目结构
```
guji-mcp-server/
├── docs/                    # 文档目录
│   ├── api/                # API文档
│   ├── examples/           # 使用示例
│   └── architecture/       # 架构设计
├── src/                    # 源代码
│   ├── guji_mcp_server/    # 主模块
│   ├── search/             # 搜索模块
│   ├── extract/            # 内容提取模块
│   └── cache/              # 缓存模块
├── tests/                  # 测试文件
├── examples/               # 示例代码
└── requirements.txt        # 依赖文件
```

### 开发环境
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 代码格式化
black src/
isort src/

# 类型检查
mypy src/
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: pp
- 邮箱: your.email@example.com
- 项目地址: https://github.com/your-username/guji-mcp-server

---

**注意**: 本项目仅用于学术研究和学习目的，请遵守相关法律法规和网站使用条款。
