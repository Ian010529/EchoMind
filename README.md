# EchoMind

EchoMind 是一个包含 Python 多 Agent 客服后端和 Vue 调试前端的完整项目。

## 目录

- `EchoMind/`：FastAPI 后端、Agent 编排、Redis/ChromaDB 记忆、RAG、Skills 与评测。
- `EchoMindFrontend/`：Vue 3 + Vite 前端控制台。

## 启动

后端：

```bash
cd EchoMind
cp .env.example .env
# 在 .env 中配置 OPENAI_API_KEY、OPENAI_MODEL=gpt-4o-mini
docker compose up -d --build redis chromadb echomind
```

前端：

```bash
cd EchoMindFrontend
npm install
npm run dev
```

默认地址：

- 前端：http://localhost:5173
- 后端：http://localhost:8000
- Swagger：http://localhost:8000/docs

`.env` 不会提交到 Git，请只在本地配置 API key。
