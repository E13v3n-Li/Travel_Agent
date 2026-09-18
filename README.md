# 智能旅游攻略助手

基于 **LangChain + LangGraph + ReAct** 的旅游攻略 Agent，支持多轮对话、工具调用、流式输出与持久化记忆。

用户只需用自然语言描述旅游需求（目的地、天数、预算、偏好等），Agent 会自动调用天气查询、景点搜索、路线规划等工具，生成可执行的旅游攻略。

---

## 📁 项目结构

```
.
├── app.py                      # Streamlit 入口
├── checkpoints.db              # SQLite 会话记忆（首次运行自动生成）
├── .env                        # 环境变量（需自行创建）
├── README.md
├── src/
│   ├── __init__.py
│   ├── agent.py                # Agent 初始化（模型 + 工具 + checkpointer）
│   └── prompt.py               # System Prompt
├── tools/
│   ├── __init__.py             # 工具注册
│   ├── weather.py              # 天气查询工具
│   ├── poi.py                  # 景点/美食/酒店搜索工具
│   └── plan.py                 # 路线规划工具
└── agent_utils/
    ├── __init__.py
    ├── geo.py                  # 城市 → 经纬度
    └── make_request.py         # 通用 HTTP 请求封装
```

---

## 🧰 环境要求

- Python **3.10+**
- 依赖包（建议用 `pip` 或 `uv` 安装）：
```bash
pip install streamlit \
            langchain langchain-core langchain-community \
            langgraph langgraph-checkpoint-sqlite \
            python-dotenv requests httpx
```

---

## 🔑 环境变量配置

在项目根目录创建 `.env` 文件：
```dotenv
# ===== 大模型配置 =====
Model=your_model_name
API_KEY=your_api_key
Base_URL=https://your-llm-endpoint/v1

# ===== System Prompt =====
SYSTEM_PROMPT=你是一个专业、可靠的旅游助手...

# ===== 高德地图（景点搜索 + 路线规划）=====
gaode_map_api_key=your_gaode_key

# ===== 天气 API（和风天气）=====
weather_api_key=your_weather_key
weather_api_host=your_weather_host
```
> 💡 高德 Key 申请：https://lbs.amap.com/
> 💡 和风天气 Key 申请：https://dev.qweather.com/


本项目使用 阿里云百炼平台（DashScope） 提供的模型，通过其 OpenAI 兼容接口 调用。

申请步骤：
    - 访问阿里云百炼平台：https://bailian.console.aliyun.com/
    - 使用阿里云账号登录（没有则先注册）
    - 进入「API-KEY 管理」页面，点击「创建我的 API-KEY」
    - 复制生成的 Key（形如 sk-xxxxxxxx），填入 .env 的 API_KEY
    - 在「模型广场」查看可用模型，把模型名填入 Model
    - 新用户通常有免费额度，超出后按 token 计费，可在控制台查看用量


---

## 🚀 运行方式

```bash
streamlit run app.py
```
浏览器打开 `http://localhost:8501`，即可开始对话。




## 🛠️ 技术栈

| 组件 | 用途 |
|---|---|
| [LangChain](https://python.langchain.com/) | LLM 抽象、消息类型、工具装饰器 |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Agent 编排、checkpointer |
| [Streamlit](https://streamlit.io/) | Web 界面 |
| [SQLite](https://www.sqlite.org/) | 会话持久化 |
| [高德地图 API](https://lbs.amap.com/) | POI 搜索、路线规划 |
| [和风天气](https://dev.qweather.com/) | 天气预报 |