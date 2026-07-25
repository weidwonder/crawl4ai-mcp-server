[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/weidwonder-crawl4ai-mcp-server-badge.png)](https://mseep.ai/app/weidwonder-crawl4ai-mcp-server)

# Crawl4AI MCP Server

[![smithery badge](https://smithery.ai/badge/@weidwonder/crawl4ai-mcp-server)](https://smithery.ai/server/@weidwonder/crawl4ai-mcp-server)

这是一个基于MCP (Model Context Protocol)的智能信息获取服务器,为AI助手系统提供强大的搜索能力和面向LLM优化的网页内容理解功能。通过多引擎搜索和智能内容提取,帮助AI系统高效获取和理解互联网信息,将网页内容转换为最适合LLM处理的格式。

## 特性

- 🔍 强大的多引擎搜索能力,支持DuckDuckGo、Google和You.com
- 📚 面向LLM优化的网页内容提取,智能过滤非核心内容
- 🎯 专注信息价值,自动识别和保留关键内容
- 📝 多种输出格式,支持引用溯源
- 🚀 基于FastMCP的高性能异步设计

## 安装

### 方式1: 大部分的安装场景

1. 确保您的系统满足以下要求:
   - Python >= 3.9
   - 建议使用专门的虚拟环境

2. 克隆仓库:
```bash
git clone https://github.com/yourusername/crawl4ai-mcp-server.git
cd crawl4ai-mcp-server
```

3. 创建并激活虚拟环境:
```bash
python -m venv crawl4ai_env
source crawl4ai_env/bin/activate  # Linux/Mac
# 或
.\crawl4ai_env\Scripts\activate  # Windows
```

4. 安装依赖:
```bash
pip install -r requirements.txt
```

5. 安装playwright浏览器:
```bash
playwright install
```

### 方式2: 安装到Claude桌面客户端 via Smithery

通过 [Smithery](https://smithery.ai/server/@weidwonder/crawl4ai-mcp-server) 将 Crawl4AI MCP 的 Claude 桌面端服务安装自动配置至您本地的 `Claude 伸展中心`:

```bash
npx -y @smithery/cli install @weidwonder/crawl4ai-mcp-server --client claude
```

## 使用方法

服务器提供以下工具:

### search
强大的网络搜索工具,支持多个搜索引擎:

- DuckDuckGo搜索(默认): 无需API密钥,全面处理AbstractText、Results和RelatedTopics
- Google搜索: 需要配置API密钥,提供精准搜索结果
- You.com搜索: 需要配置API密钥,提供高质量搜索结果
- 支持同时使用多个引擎获取更全面的结果

参数说明:
- `query`: 搜索查询字符串
- `num_results`: 返回结果数量(默认10)
- `engine`: 搜索引擎选择
  - "duckduckgo": DuckDuckGo搜索(默认)
  - "google": Google搜索(需要API密钥)
  - "youcom": You.com搜索(需要API密钥)
  - "all": 同时使用所有可用的搜索引擎

示例:
```python
# DuckDuckGo搜索(默认)
{
    "query": "python programming",
    "num_results": 5
}

# 使用所有可用引擎
{
    "query": "python programming",
    "num_results": 5,
    "engine": "all"
}
```

### read_url
面向LLM优化的网页内容理解工具,提供智能内容提取和格式转换:

- `markdown_with_citations`: 包含内联引用的Markdown(默认),保持信息溯源
- `fit_markdown`: 经过LLM优化的精简内容,去除冗余信息
- `raw_markdown`: 基础HTML→Markdown转换
- `references_markdown`: 单独的引用/参考文献部分
- `fit_html`: 生成fit_markdown的过滤后HTML
- `markdown`: 默认Markdown格式

示例:
```python
{
    "url": "https://example.com",
    "format": "markdown_with_citations"
}
```

示例:
```python
# DuckDuckGo搜索(默认)
{
    "query": "python programming",
    "num_results": 5
}

# Google搜索
{
    "query": "python programming",
    "num_results": 5,
    "engine": "google"
}
```

如需使用Google搜索,需要在config.json中配置API密钥:
```json
{
    "google": {
        "api_key": "your-api-key",
        "cse_id": "your-cse-id"
    }
}
```

如需使用You.com搜索,需要在config.json中配置API密钥:
```json
{
    "youcom": {
        "api_key": "your-youcom-api-key",
        "max_results": 10
    }
}
```

## LLM内容优化

服务器采用了一系列针对LLM的内容优化策略:

- 智能内容识别: 自动识别并保留文章主体、关键信息段落
- 噪音过滤: 自动过滤导航栏、广告、页脚等对理解无帮助的内容
- 信息完整性: 保留URL引用,支持信息溯源
- 长度优化: 使用最小词数阈值(10)过滤无效片段
- 格式优化: 默认输出markdown_with_citations格式,便于LLM理解和引用

## 开发说明

项目结构:
```
crawl4ai_mcp_server/
├── src/
│   ├── index.py      # 服务器主实现
│   └── search.py     # 搜索功能实现
├── config_demo.json  # 配置文件示例
├── pyproject.toml    # 项目配置
├── requirements.txt  # 依赖列表
└── README.md        # 项目文档
```

## 配置说明

1. 复制配置示例文件:
```bash
cp config_demo.json config.json
```

2. 如需使用Google搜索,在config.json中配置API密钥:
```json
{
    "google": {
        "api_key": "your-google-api-key",
        "cse_id": "your-google-cse-id"
    }
}
```

3. 如需使用You.com搜索,在config.json中配置API密钥:
```json
{
    "youcom": {
        "api_key": "your-youcom-api-key",
        "max_results": 10
    }
}
```

## 更新日志

- 2026.07.25: 添加You.com搜索支持,可在config.json中配置API密钥使用
- 2025.02.08: 添加搜索功能,支持DuckDuckGo(默认)和Google搜索
- 2025.02.07: 重构项目结构,使用FastMCP实现,优化依赖管理
- 2025.02.07: 优化内容过滤配置,提高token效率并保持URL完整性

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request!

## 作者

- Owner: weidwonder  
- Coder: Claude Sonnet 3.5 
    - 100% Code wrote by Claude. Cost: $9 ($2 for code writing, $7 cost for Debuging😭)
    - 3 hours time cost. 0.5 hours for code writing, 0.5 hours for env preparing, 2 hours for debuging.😭

## 致谢

感谢所有为项目做出贡献的开发者!

特别感谢:
- [Crawl4ai](https://github.com/crawl4ai/crawl4ai) 项目提供的优秀网页内容提取技术支持