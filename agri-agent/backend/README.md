# 农信智盾 - 农业金融智能体

基于 LangGraph + Ollama 构建的农业金融智能体，支持知识库检索、天气查询、农产品价格查询等功能。

## 环境要求
- Python 3.10+
- Ollama (需下载 qwen2.5:7b 和 nomic-embed-text)
-至少 8GB 内存（推荐 16GB）
-（可选）高德地图 API Key（用于实时天气）

## 快速开始

1. 安装依赖
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. 下载 Ollama 模型
\`\`\`bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
\`\`\`

3. 加载知识库（首次运行）
\`\`\`bash
python scripts/load_knowledge.py
\`\`\`

4. 启动 API 服务
\`\`\`bash
python src/server.py
\`\`\`

5. 测试
\`\`\`bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"我想贷款5万"}'
\`\`\`

## 项目结构
```
nongxin-agent/
├── config/
│   └── settings.yaml          # 配置文件（模型、API密钥等）
├── data/
│   └── knowledge/             # 知识库源文件（Markdown）
│       ├── loan_products.md
│       ├── subsidies.md
│       ├── crop_tech.md
│       └── faq.md
├── src/
│   ├── agents/
│   │   └── agent.py           # LangGraph 智能体核心逻辑
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather_tool.py    # 天气查询工具
│   │   ├── price_tool.py      # 农产品价格工具（预留）
│   │   └── rag_tool.py        # 知识库检索工具
│   ├── db/
│   │   └── vector_store.py    # 向量数据库管理
│   └── server.py              # FastAPI 服务入口
├── scripts/
│   └── load_knowledge.py      # 知识库导入脚本
├── requirements.txt
├── README.md
└── .gitignore
```
