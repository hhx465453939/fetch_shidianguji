# 搜索API接口文档

## 概述

搜索API提供古籍文本的智能检索功能，支持多种搜索模式和过滤条件，为AI助手提供精准的古籍知识检索能力。

## 基础搜索接口

### `search_ancient_texts`

**功能**: 搜索包含指定关键词的古籍文本内容

**参数**:
```python
{
    "keyword": str,              # 必需，搜索关键词
    "search_type": str,          # 可选，搜索类型 (full_text|title|author)
    "category": str,             # 可选，四部分类 (经部|史部|子部|集部|道教部|佛教部)
    "dynasty": str,              # 可选，朝代筛选
    "fuzzy": bool,               # 可选，是否模糊搜索，默认True
    "limit": int,                # 可选，返回结果数量，默认10，最大100
    "sort_by": str,              # 可选，排序方式 (relevance|dynasty|title)
    "only_main_text": bool,      # 可选，仅搜索正文，默认False
    "only_original_chars": bool  # 可选，仅搜索原字，默认False
}
```

**返回格式**:
```python
{
    "success": bool,
    "total_results": int,
    "returned_results": int,
    "search_time": float,
    "results": [
        {
            "book_id": str,
            "title": str,
            "author": str,
            "dynasty": str,
            "version": str,
            "quality": str,          # 精校|粗校
            "snippet": str,          # 包含关键词的内容片段
            "context": str,          # 上下文内容
            "source": str,           # 完整来源信息
            "page_number": int,      # 页码
            "chapter": str,          # 章节信息
            "relevance_score": float # 相关度评分
        }
    ],
    "filters_applied": {
        "category": str,
        "dynasty": str,
        "search_type": str
    }
}
```

**使用示例**:
```python
# 基础搜索
result = search_ancient_texts("道", limit=5)

# 分类搜索
result = search_ancient_texts(
    keyword="易",
    category="经部",
    dynasty="先秦",
    fuzzy=True,
    limit=10
)

# 精确搜索
result = search_ancient_texts(
    keyword="皇极经世",
    search_type="title",
    only_main_text=True,
    sort_by="dynasty"
)
```

## 高级搜索接口

### `advanced_search`

**功能**: 支持复杂查询条件的高级搜索

**参数**:
```python
{
    "query": {
        "keywords": [str],           # 多关键词搜索
        "phrases": [str],            # 短语搜索
        "exclude": [str],            # 排除关键词
        "wildcards": [str]           # 通配符搜索
    },
    "filters": {
        "categories": [str],         # 多分类筛选
        "dynasties": [str],          # 多朝代筛选
        "authors": [str],            # 作者筛选
        "date_range": {
            "start": str,            # 开始时间
            "end": str               # 结束时间
        },
        "quality_levels": [str]      # 质量等级筛选
    },
    "options": {
        "fuzzy": bool,
        "case_sensitive": bool,
        "whole_word": bool,
        "proximity": int             # 关键词邻近度
    },
    "pagination": {
        "page": int,                 # 页码，从1开始
        "page_size": int             # 每页大小
    },
    "sorting": {
        "field": str,                # 排序字段
        "order": str                 # 排序方向 (asc|desc)
    }
}
```

**返回格式**:
```python
{
    "success": bool,
    "total_results": int,
    "page": int,
    "page_size": int,
    "total_pages": int,
    "search_time": float,
    "results": [...],                # 同基础搜索的结果格式
    "facets": {                      # 聚合统计信息
        "categories": {
            "经部": 150,
            "史部": 200,
            "子部": 100
        },
        "dynasties": {
            "先秦": 50,
            "汉": 80,
            "唐": 120
        },
        "authors": {
            "孔子": 30,
            "老子": 25,
            "庄子": 20
        }
    }
}
```

## 书籍搜索接口

### `search_books`

**功能**: 搜索古籍书籍信息

**参数**:
```python
{
    "title": str,                    # 书籍标题关键词
    "author": str,                   # 作者关键词
    "dynasty": str,                  # 朝代
    "category": str,                 # 分类
    "exact_match": bool,             # 是否精确匹配
    "limit": int                     # 结果数量
}
```

**返回格式**:
```python
{
    "success": bool,
    "total_results": int,
    "books": [
        {
            "book_id": str,
            "title": str,
            "author": str,
            "dynasty": str,
            "category": str,
            "description": str,
            "version_info": str,
            "quality": str,
            "total_chapters": int,
            "total_pages": int,
            "last_updated": str,
            "tags": [str]
        }
    ]
}
```

## 作者搜索接口

### `search_authors`

**功能**: 搜索古籍作者信息

**参数**:
```python
{
    "name": str,                     # 作者姓名关键词
    "dynasty": str,                  # 朝代
    "category": str,                 # 主要分类
    "limit": int                     # 结果数量
}
```

**返回格式**:
```python
{
    "success": bool,
    "total_results": int,
    "authors": [
        {
            "author_id": str,
            "name": str,
            "dynasty": str,
            "birth_year": str,
            "death_year": str,
            "biography": str,
            "main_works": [str],
            "categories": [str],
            "total_works": int
        }
    ]
}
```

## 搜索建议接口

### `get_search_suggestions`

**功能**: 获取搜索建议和自动补全

**参数**:
```python
{
    "query": str,                    # 查询字符串
    "type": str,                     # 建议类型 (keyword|title|author)
    "limit": int                     # 建议数量
}
```

**返回格式**:
```python
{
    "success": bool,
    "suggestions": [
        {
            "text": str,             # 建议文本
            "type": str,             # 类型
            "frequency": int,        # 出现频率
            "category": str          # 分类
        }
    ]
}
```

## 搜索统计接口

### `get_search_statistics`

**功能**: 获取搜索统计信息

**参数**:
```python
{
    "time_range": str,               # 时间范围 (day|week|month|year)
    "category": str,                 # 分类筛选
    "dynasty": str                   # 朝代筛选
}
```

**返回格式**:
```python
{
    "success": bool,
    "statistics": {
        "total_searches": int,
        "unique_keywords": int,
        "most_searched": [str],
        "category_distribution": dict,
        "dynasty_distribution": dict,
        "search_trends": [
            {
                "date": str,
                "count": int
            }
        ]
    }
}
```

## 错误处理

### 错误码定义

| 错误码 | 错误信息 | 描述 |
|--------|----------|------|
| 400 | INVALID_PARAMETER | 参数无效 |
| 401 | UNAUTHORIZED | 未授权访问 |
| 403 | FORBIDDEN | 禁止访问 |
| 404 | NOT_FOUND | 资源未找到 |
| 429 | RATE_LIMIT_EXCEEDED | 请求频率超限 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |
| 503 | SERVICE_UNAVAILABLE | 服务不可用 |

### 错误响应格式

```python
{
    "success": False,
    "error": {
        "code": str,
        "message": str,
        "details": str,
        "timestamp": str
    }
}
```

## 使用限制

### 频率限制

| 接口类型 | 限制 | 时间窗口 |
|----------|------|----------|
| 基础搜索 | 10次/分钟 | 1分钟 |
| 高级搜索 | 5次/分钟 | 1分钟 |
| 书籍搜索 | 20次/分钟 | 1分钟 |
| 作者搜索 | 15次/分钟 | 1分钟 |

### 结果限制

- 单次搜索最大返回结果数: 100
- 关键词最大长度: 100字符
- 高级搜索最大关键词数: 10个
- 分页最大页数: 100页

## 最佳实践

### 搜索优化

1. **使用精确的关键词**: 避免过于宽泛的搜索词
2. **合理使用过滤条件**: 通过分类和朝代缩小搜索范围
3. **利用模糊搜索**: 对于不确定的词汇使用模糊搜索
4. **控制结果数量**: 根据需求设置合适的limit值

### 性能优化

1. **缓存搜索结果**: 相同查询优先使用缓存
2. **批量搜索**: 多个相关查询可以合并处理
3. **异步处理**: 大量搜索请求使用异步处理
4. **分页加载**: 大量结果使用分页加载

### 错误处理

1. **重试机制**: 网络错误时自动重试
2. **降级策略**: 服务不可用时返回缓存结果
3. **用户提示**: 提供清晰的错误信息和建议
4. **日志记录**: 记录详细的错误日志用于调试
