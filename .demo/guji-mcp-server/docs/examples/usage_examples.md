# 使用示例和最佳实践

## 基础使用示例

### 1. 简单搜索示例

```python
# 基础关键词搜索
from guji_mcp_server import GujiMCPServer

# 初始化服务器
server = GujiMCPServer()

# 搜索包含"道"的古籍内容
result = await server.search_ancient_texts(
    keyword="道",
    limit=5
)

print(f"找到 {result['total_results']} 条结果")
for item in result['results']:
    print(f"书名: {item['title']}")
    print(f"作者: {item['author']}")
    print(f"朝代: {item['dynasty']}")
    print(f"内容片段: {item['snippet']}")
    print("---")
```

### 2. 分类搜索示例

```python
# 在经部中搜索"易"相关内容
result = await server.search_ancient_texts(
    keyword="易",
    category="经部",
    dynasty="先秦",
    fuzzy=True,
    limit=10
)

# 在史部中搜索"史记"相关内容
result = await server.search_ancient_texts(
    keyword="史记",
    category="史部",
    search_type="title",
    limit=5
)
```

### 3. 内容提取示例

```python
# 获取书籍详细信息
book_info = await server.extract_book_info("HY1523")
print(f"书名: {book_info['title']}")
print(f"作者: {book_info['author']}")
print(f"总章节数: {book_info['metadata']['total_chapters']}")

# 提取包含特定关键词的内容片段
snippets = await server.extract_content_snippets(
    book_id="HY1523",
    keyword="皇极经世",
    context_length=300,
    max_snippets=5
)

for snippet in snippets['snippets']:
    print(f"章节: {snippet['chapter']}")
    print(f"页码: {snippet['page_number']}")
    print(f"内容: {snippet['highlighted_content']}")
    print("---")
```

## 高级使用示例

### 1. 批量搜索和处理

```python
import asyncio
from typing import List

async def batch_search_and_analyze(keywords: List[str]):
    """批量搜索并分析结果"""
    server = GujiMCPServer()
    all_results = []
    
    # 并发执行多个搜索
    tasks = [
        server.search_ancient_texts(keyword, limit=10)
        for keyword in keywords
    ]
    
    results = await asyncio.gather(*tasks)
    
    # 合并和分析结果
    for i, result in enumerate(results):
        print(f"关键词 '{keywords[i]}' 找到 {result['total_results']} 条结果")
        all_results.extend(result['results'])
    
    # 去重和排序
    unique_results = remove_duplicates(all_results)
    sorted_results = sort_by_relevance(unique_results)
    
    return sorted_results

# 使用示例
keywords = ["道", "德", "仁", "义", "礼"]
results = await batch_search_and_analyze(keywords)
```

### 2. 智能内容分析

```python
async def intelligent_content_analysis(book_id: str, theme: str):
    """智能内容分析"""
    server = GujiMCPServer()
    
    # 1. 搜索相关主题内容
    search_results = await server.search_ancient_texts(
        keyword=theme,
        limit=20
    )
    
    # 2. 提取详细内容
    detailed_contents = []
    for result in search_results['results']:
        if result['book_id'] == book_id:
            content = await server.get_chapter_content(
                book_id=book_id,
                chapter_id=result['chapter_id']
            )
            detailed_contents.append(content)
    
    # 3. 分析内容主题
    analysis = await server.analyze_content(
        book_id=book_id,
        analysis_type="themes",
        content_scope="full"
    )
    
    # 4. 生成分析报告
    report = generate_analysis_report(
        search_results, detailed_contents, analysis
    )
    
    return report

# 使用示例
analysis = await intelligent_content_analysis("HY1523", "皇极经世")
```

### 3. 知识图谱构建

```python
async def build_knowledge_graph(seed_keywords: List[str]):
    """构建古籍知识图谱"""
    server = GujiMCPServer()
    graph = {}
    
    for keyword in seed_keywords:
        # 搜索相关内容
        results = await server.search_ancient_texts(
            keyword=keyword,
            limit=50
        )
        
        # 提取相关实体
        entities = extract_entities(results['results'])
        
        # 建立关联关系
        for entity in entities:
            if entity not in graph:
                graph[entity] = {
                    'related_entities': set(),
                    'books': set(),
                    'frequency': 0
                }
            
            graph[entity]['related_entities'].update(entities)
            graph[entity]['books'].update([r['book_id'] for r in results['results']])
            graph[entity]['frequency'] += 1
    
    return graph

# 使用示例
seed_keywords = ["道", "德", "仁", "义", "礼", "智", "信"]
knowledge_graph = await build_knowledge_graph(seed_keywords)
```

## AI助手集成示例

### 1. Claude集成

```python
# Claude MCP配置
{
  "mcpServers": {
    "guji-server": {
      "command": "python",
      "args": ["-m", "guji_mcp_server"],
      "cwd": "/path/to/guji-mcp-server",
      "env": {
        "MCP_SERVER_HOST": "localhost",
        "MCP_SERVER_PORT": "8000"
      }
    }
  }
}
```

### 2. 对话上下文增强

```python
class GujiContextEnhancer:
    """古籍上下文增强器"""
    
    def __init__(self, mcp_server):
        self.server = mcp_server
        self.context_cache = {}
    
    async def enhance_context(self, user_query: str, context_length: int = 3):
        """增强对话上下文"""
        # 提取查询中的关键词
        keywords = extract_keywords(user_query)
        
        # 搜索相关古籍内容
        relevant_contents = []
        for keyword in keywords:
            results = await self.server.search_ancient_texts(
                keyword=keyword,
                limit=context_length
            )
            relevant_contents.extend(results['results'])
        
        # 格式化上下文
        context = self.format_context(relevant_contents)
        
        return context
    
    def format_context(self, contents):
        """格式化上下文内容"""
        context_parts = []
        
        for content in contents:
            context_parts.append(f"""
**来源**: {content['title']} - {content['author']} ({content['dynasty']})
**内容**: {content['snippet']}
**相关度**: {content['relevance_score']:.2f}
---
            """)
        
        return "\n".join(context_parts)

# 使用示例
enhancer = GujiContextEnhancer(server)
context = await enhancer.enhance_context("请解释一下道家的思想", context_length=5)
```

### 3. 智能问答系统

```python
class GujiQASystem:
    """古籍智能问答系统"""
    
    def __init__(self, mcp_server):
        self.server = mcp_server
        self.qa_cache = {}
    
    async def answer_question(self, question: str):
        """回答古籍相关问题"""
        # 1. 分析问题类型
        question_type = self.classify_question(question)
        
        # 2. 提取关键词
        keywords = self.extract_keywords(question)
        
        # 3. 搜索相关内容
        search_results = []
        for keyword in keywords:
            results = await self.server.search_ancient_texts(
                keyword=keyword,
                limit=10
            )
            search_results.extend(results['results'])
        
        # 4. 生成答案
        if question_type == "definition":
            answer = self.generate_definition_answer(search_results)
        elif question_type == "comparison":
            answer = self.generate_comparison_answer(search_results)
        elif question_type == "explanation":
            answer = self.generate_explanation_answer(search_results)
        else:
            answer = self.generate_general_answer(search_results)
        
        # 5. 添加引用信息
        answer_with_citations = self.add_citations(answer, search_results)
        
        return answer_with_citations
    
    def classify_question(self, question: str) -> str:
        """分类问题类型"""
        if any(word in question for word in ["是什么", "定义", "含义"]):
            return "definition"
        elif any(word in question for word in ["比较", "区别", "差异"]):
            return "comparison"
        elif any(word in question for word in ["解释", "说明", "阐述"]):
            return "explanation"
        else:
            return "general"

# 使用示例
qa_system = GujiQASystem(server)
answer = await qa_system.answer_question("道家的核心思想是什么？")
print(answer)
```

## 性能优化示例

### 1. 缓存策略优化

```python
class OptimizedGujiServer:
    """优化的古籍服务器"""
    
    def __init__(self):
        self.server = GujiMCPServer()
        self.cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0
        }
    
    async def cached_search(self, keyword: str, **kwargs):
        """带缓存的搜索"""
        cache_key = f"search:{hash(str((keyword, kwargs)))}"
        
        # 检查缓存
        if cache_key in self.cache:
            self.cache_stats['hits'] += 1
            return self.cache[cache_key]
        
        # 执行搜索
        result = await self.server.search_ancient_texts(keyword, **kwargs)
        
        # 缓存结果
        self.cache[cache_key] = result
        self.cache_stats['misses'] += 1
        
        return result
    
    def get_cache_stats(self):
        """获取缓存统计"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = self.cache_stats['hits'] / total if total > 0 else 0
        return {
            'hit_rate': hit_rate,
            'total_requests': total,
            'cache_size': len(self.cache)
        }
```

### 2. 并发处理优化

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ConcurrentGujiServer:
    """并发处理的古籍服务器"""
    
    def __init__(self, max_workers=5):
        self.server = GujiMCPServer()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def parallel_search(self, queries: List[dict]):
        """并行搜索多个查询"""
        tasks = []
        
        for query in queries:
            task = asyncio.create_task(
                self.server.search_ancient_texts(**query)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"查询 {i} 失败: {result}")
                processed_results.append(None)
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def batch_extract_content(self, book_ids: List[str], keyword: str):
        """批量提取内容"""
        tasks = []
        
        for book_id in book_ids:
            task = asyncio.create_task(
                self.server.extract_content_snippets(book_id, keyword)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
```

## 错误处理和重试示例

### 1. 智能重试机制

```python
import asyncio
import random
from typing import Callable, Any

class RetryableGujiServer:
    """支持重试的古籍服务器"""
    
    def __init__(self, max_retries=3, base_delay=1.0):
        self.server = GujiMCPServer()
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """指数退避重试"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    # 计算延迟时间（指数退避 + 随机抖动）
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"尝试 {attempt + 1} 失败，{delay:.2f}秒后重试: {e}")
                    await asyncio.sleep(delay)
                else:
                    print(f"所有重试失败: {e}")
        
        raise last_exception
    
    async def robust_search(self, keyword: str, **kwargs):
        """健壮的搜索方法"""
        return await self.retry_with_backoff(
            self.server.search_ancient_texts,
            keyword,
            **kwargs
        )
```

### 2. 降级策略

```python
class FallbackGujiServer:
    """支持降级的古籍服务器"""
    
    def __init__(self):
        self.server = GujiMCPServer()
        self.fallback_data = self.load_fallback_data()
    
    def load_fallback_data(self):
        """加载降级数据"""
        # 加载一些常用的古籍内容作为降级数据
        return {
            "道": ["道德经相关片段..."],
            "德": ["道德经相关片段..."],
            "仁": ["论语相关片段..."]
        }
    
    async def search_with_fallback(self, keyword: str, **kwargs):
        """带降级的搜索"""
        try:
            # 尝试正常搜索
            result = await self.server.search_ancient_texts(keyword, **kwargs)
            return result
        except Exception as e:
            print(f"搜索失败，使用降级数据: {e}")
            
            # 使用降级数据
            fallback_content = self.fallback_data.get(keyword, [])
            return {
                "success": True,
                "total_results": len(fallback_content),
                "returned_results": len(fallback_content),
                "search_time": 0.0,
                "results": [
                    {
                        "book_id": "fallback",
                        "title": "降级数据",
                        "author": "未知",
                        "dynasty": "未知",
                        "snippet": content,
                        "relevance_score": 0.5
                    }
                    for content in fallback_content
                ],
                "fallback": True
            }
```

## 监控和调试示例

### 1. 性能监控

```python
import time
import logging
from functools import wraps

class MonitoredGujiServer:
    """带监控的古籍服务器"""
    
    def __init__(self):
        self.server = GujiMCPServer()
        self.logger = logging.getLogger(__name__)
        self.metrics = {
            'search_count': 0,
            'extract_count': 0,
            'total_time': 0.0,
            'error_count': 0
        }
    
    def monitor_performance(self, func):
        """性能监控装饰器"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                self.metrics['search_count'] += 1
                return result
            except Exception as e:
                self.metrics['error_count'] += 1
                self.logger.error(f"操作失败: {e}")
                raise
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                self.metrics['total_time'] += execution_time
                self.logger.info(f"{func.__name__} 执行时间: {execution_time:.2f}秒")
        
        return wrapper
    
    @monitor_performance
    async def search_ancient_texts(self, keyword: str, **kwargs):
        """监控的搜索方法"""
        return await self.server.search_ancient_texts(keyword, **kwargs)
    
    def get_metrics(self):
        """获取性能指标"""
        avg_time = self.metrics['total_time'] / max(self.metrics['search_count'], 1)
        return {
            'total_searches': self.metrics['search_count'],
            'total_errors': self.metrics['error_count'],
            'average_response_time': avg_time,
            'error_rate': self.metrics['error_count'] / max(self.metrics['search_count'], 1)
        }
```

### 2. 调试工具

```python
class DebugGujiServer:
    """调试版古籍服务器"""
    
    def __init__(self, debug=True):
        self.server = GujiMCPServer()
        self.debug = debug
        self.debug_log = []
    
    def log_debug(self, message: str, data: dict = None):
        """记录调试信息"""
        if self.debug:
            debug_entry = {
                'timestamp': time.time(),
                'message': message,
                'data': data
            }
            self.debug_log.append(debug_entry)
            print(f"[DEBUG] {message}")
            if data:
                print(f"[DEBUG] 数据: {data}")
    
    async def debug_search(self, keyword: str, **kwargs):
        """调试搜索"""
        self.log_debug(f"开始搜索: {keyword}", kwargs)
        
        try:
            result = await self.server.search_ancient_texts(keyword, **kwargs)
            self.log_debug(f"搜索成功: {result['total_results']} 条结果")
            return result
        except Exception as e:
            self.log_debug(f"搜索失败: {e}")
            raise
    
    def get_debug_log(self):
        """获取调试日志"""
        return self.debug_log
    
    def clear_debug_log(self):
        """清除调试日志"""
        self.debug_log.clear()
```

这些示例展示了如何使用古籍MCP服务器进行各种操作，包括基础搜索、高级分析、AI集成、性能优化、错误处理和监控调试。通过这些示例，开发者可以快速上手并构建自己的古籍知识应用。
