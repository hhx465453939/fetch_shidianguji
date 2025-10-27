# 内容提取API接口文档

## 概述

内容提取API提供古籍内容的详细提取功能，包括书籍信息、章节内容、内容片段等，为AI助手提供完整的古籍文献支持。

## 书籍信息提取

### `extract_book_info`

**功能**: 提取指定书籍的详细信息

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "include_chapters": bool,       # 可选，是否包含章节列表，默认True
    "include_metadata": bool,       # 可选，是否包含元数据，默认True
    "include_statistics": bool      # 可选，是否包含统计信息，默认False
}
```

**返回格式**:
```python
{
    "success": bool,
    "book_info": {
        "book_id": str,
        "title": str,
        "author": str,
        "dynasty": str,
        "category": str,
        "description": str,
        "version_info": {
            "publisher": str,
            "year": str,
            "edition": str,
            "quality": str          # 精校|粗校
        },
        "metadata": {
            "total_chapters": int,
            "total_pages": int,
            "total_characters": int,
            "language": str,
            "script_type": str,     # 简体|繁体
            "last_updated": str
        },
        "chapters": [               # 当include_chapters=True时
            {
                "chapter_id": str,
                "title": str,
                "page_number": int,
                "word_count": int,
                "summary": str
            }
        ],
        "statistics": {             # 当include_statistics=True时
            "average_chapter_length": int,
            "longest_chapter": str,
            "shortest_chapter": str,
            "complexity_score": float
        }
    }
}
```

**使用示例**:
```python
# 基础书籍信息
book_info = extract_book_info("HY1523")

# 包含统计信息
book_info = extract_book_info(
    book_id="HY1523",
    include_statistics=True
)
```

## 内容片段提取

### `extract_content_snippets`

**功能**: 提取包含指定关键词的内容片段

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "keyword": str,                 # 必需，关键词
    "context_length": int,          # 可选，上下文长度，默认200字符
    "max_snippets": int,            # 可选，最大片段数，默认10
    "include_page_info": bool,      # 可选，是否包含页码信息，默认True
    "highlight_keyword": bool       # 可选，是否高亮关键词，默认True
}
```

**返回格式**:
```python
{
    "success": bool,
    "book_id": str,
    "keyword": str,
    "total_matches": int,
    "snippets": [
        {
            "snippet_id": str,
            "content": str,          # 内容片段
            "highlighted_content": str,  # 高亮后的内容
            "context_before": str,   # 前文
            "context_after": str,    # 后文
            "page_number": int,      # 页码
            "chapter": str,          # 章节
            "position": int,         # 在章节中的位置
            "relevance_score": float # 相关度评分
        }
    ]
}
```

**使用示例**:
```python
# 基础内容片段提取
snippets = extract_content_snippets(
    book_id="HY1523",
    keyword="皇极经世"
)

# 详细内容片段提取
snippets = extract_content_snippets(
    book_id="HY1523",
    keyword="道",
    context_length=300,
    max_snippets=5,
    highlight_keyword=True
)
```

## 章节内容提取

### `get_chapter_content`

**功能**: 获取指定章节的完整内容

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "chapter_id": str,              # 必需，章节ID
    "format": str,                  # 可选，格式 (markdown|html|plain)，默认markdown
    "include_annotations": bool,    # 可选，是否包含注释，默认False
    "include_translation": bool     # 可选，是否包含翻译，默认False
}
```

**返回格式**:
```python
{
    "success": bool,
    "chapter_info": {
        "book_id": str,
        "chapter_id": str,
        "title": str,
        "page_number": int,
        "word_count": int,
        "character_count": int
    },
    "content": str,                 # 章节内容
    "annotations": [                # 当include_annotations=True时
        {
            "position": int,
            "text": str,
            "annotation": str,
            "type": str             # 注释|翻译|解释
        }
    ],
    "metadata": {
        "extraction_time": str,
        "format": str,
        "encoding": str
    }
}
```

## 多章节批量提取

### `extract_multiple_chapters`

**功能**: 批量提取多个章节的内容

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "chapter_ids": [str],           # 必需，章节ID列表
    "format": str,                  # 可选，格式，默认markdown
    "parallel": bool,               # 可选，是否并行处理，默认True
    "max_workers": int              # 可选，最大工作线程数，默认5
}
```

**返回格式**:
```python
{
    "success": bool,
    "book_id": str,
    "total_chapters": int,
    "successful_extractions": int,
    "failed_extractions": int,
    "chapters": [
        {
            "chapter_id": str,
            "success": bool,
            "content": str,          # 成功时
            "error": str,            # 失败时
            "extraction_time": float
        }
    ],
    "summary": {
        "total_time": float,
        "average_time_per_chapter": float
    }
}
```

## 全文提取

### `extract_full_text`

**功能**: 提取整本书的完整内容

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "format": str,                  # 可选，格式，默认markdown
    "include_toc": bool,            # 可选，是否包含目录，默认True
    "include_metadata": bool,       # 可选，是否包含元数据，默认True
    "chunk_size": int,              # 可选，分块大小，默认1000字符
    "parallel": bool                # 可选，是否并行处理，默认True
}
```

**返回格式**:
```python
{
    "success": bool,
    "book_id": str,
    "full_text": str,               # 完整文本内容
    "metadata": {
        "total_chapters": int,
        "total_pages": int,
        "total_characters": int,
        "extraction_time": str,
        "format": str
    },
    "table_of_contents": [          # 当include_toc=True时
        {
            "chapter_id": str,
            "title": str,
            "page_number": int,
            "level": int
        }
    ],
    "chunks": [                     # 分块信息
        {
            "chunk_id": str,
            "chapter_id": str,
            "start_position": int,
            "end_position": int,
            "content_preview": str
        }
    ]
}
```

## 智能内容分析

### `analyze_content`

**功能**: 对提取的内容进行智能分析

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "analysis_type": str,           # 必需，分析类型 (keywords|themes|structure|sentiment)
    "content_scope": str,           # 可选，内容范围 (full|chapter|snippet)
    "chapter_id": str,              # 当content_scope=chapter时必需
    "depth": str                    # 可选，分析深度 (basic|detailed|comprehensive)
}
```

**返回格式**:
```python
{
    "success": bool,
    "book_id": str,
    "analysis_type": str,
    "analysis_result": {
        "keywords": [               # 关键词分析
            {
                "keyword": str,
                "frequency": int,
                "importance": float,
                "contexts": [str]
            }
        ],
        "themes": [                 # 主题分析
            {
                "theme": str,
                "description": str,
                "relevance_score": float,
                "related_keywords": [str]
            }
        ],
        "structure": {              # 结构分析
            "total_sections": int,
            "average_section_length": int,
            "complexity_metrics": dict
        },
        "sentiment": {              # 情感分析
            "overall_sentiment": str,
            "sentiment_score": float,
            "emotional_keywords": [str]
        }
    }
}
```

## 内容格式化

### `format_content`

**功能**: 对提取的内容进行格式化处理

**参数**:
```python
{
    "content": str,                 # 必需，原始内容
    "format_type": str,             # 必需，格式类型 (markdown|html|plain|ancient)
    "options": {
        "preserve_structure": bool,  # 是否保持原有结构
        "add_line_numbers": bool,   # 是否添加行号
        "highlight_keywords": [str], # 高亮关键词
        "add_annotations": bool,    # 是否添加注释
        "modernize_punctuation": bool # 是否现代化标点
    }
}
```

**返回格式**:
```python
{
    "success": bool,
    "formatted_content": str,       # 格式化后的内容
    "format_info": {
        "original_length": int,
        "formatted_length": int,
        "format_type": str,
        "processing_time": float
    }
}
```

## 内容验证

### `validate_content`

**功能**: 验证提取内容的完整性和质量

**参数**:
```python
{
    "book_id": str,                 # 必需，书籍ID
    "content_type": str,            # 必需，内容类型 (full|chapter|snippet)
    "validation_level": str         # 可选，验证级别 (basic|standard|strict)
}
```

**返回格式**:
```python
{
    "success": bool,
    "validation_result": {
        "is_valid": bool,
        "quality_score": float,     # 质量评分 (0-100)
        "issues": [
            {
                "type": str,        # 问题类型
                "severity": str,    # 严重程度
                "description": str,
                "position": int,    # 问题位置
                "suggestion": str   # 修复建议
            }
        ],
        "statistics": {
            "total_characters": int,
            "valid_characters": int,
            "encoding_issues": int,
            "format_issues": int
        }
    }
}
```

## 错误处理

### 常见错误

| 错误码 | 错误信息 | 描述 |
|--------|----------|------|
| 400 | INVALID_BOOK_ID | 无效的书籍ID |
| 400 | INVALID_CHAPTER_ID | 无效的章节ID |
| 404 | BOOK_NOT_FOUND | 书籍不存在 |
| 404 | CHAPTER_NOT_FOUND | 章节不存在 |
| 429 | EXTRACTION_LIMIT_EXCEEDED | 提取频率超限 |
| 500 | EXTRACTION_FAILED | 内容提取失败 |
| 503 | CONTENT_UNAVAILABLE | 内容不可用 |

## 使用限制

### 频率限制

| 操作类型 | 限制 | 时间窗口 |
|----------|------|----------|
| 书籍信息提取 | 30次/分钟 | 1分钟 |
| 内容片段提取 | 20次/分钟 | 1分钟 |
| 章节内容提取 | 15次/分钟 | 1分钟 |
| 全文提取 | 5次/小时 | 1小时 |

### 内容限制

- 单次提取最大内容长度: 1MB
- 批量提取最大章节数: 50个
- 内容片段最大长度: 10KB
- 并行处理最大线程数: 10个

## 最佳实践

### 提取优化

1. **合理选择提取范围**: 根据需要选择章节或全文提取
2. **使用并行处理**: 大量内容提取时启用并行处理
3. **缓存提取结果**: 避免重复提取相同内容
4. **分块处理**: 大文件使用分块处理避免内存问题

### 内容质量

1. **验证提取结果**: 提取后验证内容完整性
2. **格式化处理**: 根据需要选择合适的格式
3. **错误处理**: 实现完善的错误处理和重试机制
4. **性能监控**: 监控提取性能和质量指标
