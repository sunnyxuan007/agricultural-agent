# 农信智盾 —— 农业金融智能体

**农信智盾** 是一套面向农户的智能服务平台，由**微信小程序前端**和**基于 LangGraph + Ollama 的本地智能体后端**组成。  
平台能够为农户提供**贷款产品推荐、农业补贴查询、种植技术指导、实时天气预警**等一站式服务。  
项目以自然语言对话为核心，帮助农民打破信息壁垒，让每一个农户都能拥有“懂农业、懂金融、懂市场”的AI助手。

## 📁 项目结构
农信智盾/
├── frontend/ # 微信小程序前端（完整源码）
│ ├── pages/ # 页面目录
│ │ └── chat/ # 核心对话页面
│ │ ├── chat.js # 对话逻辑与接口调用
│ │ ├── chat.json # 页面配置
│ │ ├── chat.wxml # 页面结构
│ │ └── chat.wxss # 页面样式
│ ├── utils/
│ │ └── api.js # 后端API请求封装（需修改地址）
│ ├── app.js # 小程序入口
│ ├── app.json # 小程序全局配置
│ ├── project.config.json # 项目配置（含AppID）
│ └── project.private.config.json # 私有配置
└── nongxin-agent(backend)/ # 智能体后端服务（LangGraph + Ollama）
├── config/ # 配置文件（需修改天气API）
├── data/knowledge/ # 知识库（Markdown文件）
├── src/ # 后端源码
│ ├── agents/agent.py # LangGraph 智能体核心
│ ├── tools/ # 工具模块（天气、知识库检索）
│ ├── db/vector_store.py # 向量数据库管理
│ └── server.py # FastAPI 服务入口
├── scripts/load_knowledge.py # 知识库初始化脚本
└── requirements.txt # Python依赖


## 📁 配置并运行小程序
用微信开发者工具打开 frontend 文件夹

修改 utils/api.js 中的 BASE_URL：

模拟器调试：http://localhost:8000

真机调试（需与电脑同一WiFi）：http://你的电脑IP:8000  或ngrok地址

点击开发者工具右上角「详情」→「本地设置」→ 勾选 “不校验合法域名”

点击「编译」即可预览；点击「预览」生成二维码，手机扫码体验。


## 🔧 技术栈
前端：微信小程序原生框架

后端：Python + FastAPI + LangGraph

本地模型：Ollama + Qwen 7B

向量数据库：ChromaDB (RAG)

外部API：高德天气（可选）


## 📌 注意事项
首次加载知识库需要一定时间（取决于文档数量），请耐心等待 load_knowledge.py 执行完成。

天气功能需要申请高德API Key（免费），若不配置则返回模拟数据，不影响其他功能。

真机调试时，确保手机与电脑连接同一WiFi，并且关闭Windows防火墙或允许8000端口入站。


## 📄 许可证
本项目采用 MIT 许可证，详情见 LICENSE 文件。

## 🤝 贡献与支持
欢迎提交 Issue 和 Pull Request。
项目开发团队：致富路上不掉队


农信智盾 —— 让科技扎根土地，让农民享受数字金融的便利。