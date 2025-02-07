# Crawl4AI MCP Server

这是一个基于MCP (Model Context Protocol)的网页爬虫服务器,提供高效的网页内容抓取和转换功能。该服务器专门设计用于AI助手系统,能够将网页内容转换为多种格式,优化后用于上下文输入。

## 特性

- 🚀 基于FastMCP实现的高性能服务器
- 🎯 智能内容过滤,专注于核心内容
- 📝 多种输出格式支持
- 🔗 保留引用完整性
- 🛠 异步操作设计

## 安装

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

## 使用方法

服务器提供以下工具:

### read_url
网页内容抓取工具,支持以下输出格式:

- `raw_markdown`: 基础HTML→Markdown转换
- `markdown_with_citations`: 包含内联引用的Markdown(默认)
- `references_markdown`: 引用/参考文献部分
- `fit_markdown`: 经过内容过滤的Markdown
- `fit_html`: 生成fit_markdown的过滤后HTML
- `markdown`: 默认Markdown格式

示例:
```python
{
    "url": "https://example.com",
    "format": "markdown_with_citations"
}
```

### search
网络搜索工具,支持多个搜索引擎:

- DuckDuckGo搜索(默认)
- Google搜索(需要配置API密钥)

参数说明:
- `query`: 搜索查询字符串
- `num_results`: 返回结果数量(默认10)
- `engine`: 搜索引擎选择
  - "duckduckgo": DuckDuckGo搜索(默认)
  - "google": Google搜索(需要API密钥)

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

## 内容优化配置

服务器采用了以下优化配置以提供更好的内容质量:

- 最小词数阈值:10
- 自动排除导航栏、页脚、页眉等非核心内容
- 启用引用保留以保持URL信息完整性
- 默认使用 markdown_with_citations 格式输出

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

## 更新日志

- 2025.02.08: 添加搜索功能,支持DuckDuckGo(默认)和Google搜索
- 2025.02.07: 重构项目结构,使用FastMCP实现,优化依赖管理
- 2025.02.07: 优化内容过滤配置,提高token效率并保持URL完整性

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request!

## 作者

PM: weidwonder
Coder: Claude Sonnet 3.5

## 致谢

感谢所有为项目做出贡献的开发者!