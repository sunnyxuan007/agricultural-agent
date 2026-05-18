import re
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOllama
from typing import TypedDict, List
from ..tools.rag_tool import search_knowledge
from ..tools.weather_tool import get_weather   # 导入天气工具

llm = ChatOllama(model="qwen:7b", temperature=0.7)

class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]

def extract_city(query: str) -> str:
    """从用户问题中提取城市名称，如果没有则返回默认城市（佛山）"""
    # 简单正则匹配：常见模式 “在...的天气”、“...天气”
    match = re.search(r'在?([\u4e00-\u9fa5]{2,}?)(?:市|地区|省|县|区)?的?天气', query)
    if match:
        return match.group(1)
    # 也可以直接匹配城市名字典（可扩展）
    cities = ["北京", "上海", "广州", "深圳", "成都", "杭州", "武汉", "西安", "重庆", "天津", "南京", "郑州", "长沙", "沈阳", "青岛", "佛山"]
    for city in cities:
        if city in query:
            return city
    return "佛山"   # 默认城市

def call_model(state: AgentState):
    # 获取用户最后一条消息
    last_msg = state["messages"][-1] if state["messages"] else None
    if not last_msg or not isinstance(last_msg, HumanMessage):
        return {"messages": [AIMessage(content="请提出您的问题。")]}

    user_query = last_msg.content

    # --- 1. 天气意图检测与实时天气查询 ---
    if any(keyword in user_query for keyword in ["天气", "气象", "气温", "会不会下雨", "温度"]):
        city = extract_city(user_query)
        weather_info = get_weather.invoke({"city": city})
        # 可以只返回天气信息，也可以交给模型润色（这里直接返回，更快）
        answer = f"【实时天气】{weather_info}"
        return {"messages": [AIMessage(content=answer)]}

    # --- 2. 其他问题：知识库检索 + 模型生成 ---
    # 检索知识库
    try:
        search_result = search_knowledge.invoke({"query": user_query})
        context = search_result if search_result else "未找到相关知识。"
    except Exception as e:
        print(f"知识库检索失败: {e}")
        context = "知识库检索暂时不可用。"

    # 构建提示词（强制使用知识库）
    prompt = f"""你是农业金融助手“农信智盾”。请严格基于下面的【农业知识库参考内容】回答问题。

【农业知识库参考内容】
{context}

【农户问题】
{user_query}

要求：
- 优先使用知识库内容，不要编造。
- 如果知识库中找不到答案，请明确说“知识库中暂无相关信息，建议咨询当地农业部门或银行网点”。
- 回答应亲切、接地气。

请回答："""

    try:
        response = llm.invoke(prompt)
        answer = response.content
    except Exception as e:
        print(f"模型调用失败: {e}")
        answer = "抱歉，我暂时无法回答，请稍后再试。"

    return {"messages": [AIMessage(content=answer)]}

# 构建工作流
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
graph = workflow.compile()