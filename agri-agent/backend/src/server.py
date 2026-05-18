import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage   # 关键：导入正确的消息类型
from src.agents.agent import graph

app = FastAPI(title="农信智盾 API")

class Query(BaseModel):
    message: str

@app.post("/chat")
async def chat(query: Query):
    user_message = query.message
    try:
        # 构造正确的消息格式：HumanMessage 对象列表
        state = {"messages": [HumanMessage(content=query.message)]}
        result = await graph.ainvoke(state)
        messages = result.get("messages", [])
        if not messages:
            return {"answer": "智能体未返回有效回答，请稍后重试。"}
        # 取最后一条 AI 消息
        last_msg = messages[-1]
        answer = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
        return {"answer": answer}
    except Exception as e:
        print(f"请求处理异常: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)