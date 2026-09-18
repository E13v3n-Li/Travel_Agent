import uuid
import streamlit as st
from src.agent import init_agent
from langchain_core.messages import AIMessageChunk

st.set_page_config(page_title="旅游助手")
st.title("智能旅游攻略助手")
st.caption("基于 LangChain + Langgraph + ReAct 的旅游攻略 Agent 助手")
st.divider()

# 1. 初始化 Agent
if "agent" not in st.session_state:
    st.session_state["agent"] = init_agent()

# 2. 每个会话一个 thread_id
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

# 3. 消息历史
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 4. 渲染历史
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 5. 用户输入
prompt = st.chat_input("请输入你的旅游需求...")

if prompt:
    # 显示用户消息
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 调用 Agent
    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        with st.spinner("智能客服思考中..."):
            for chunk in st.session_state["agent"].stream(
                {"messages": [{"role": "user", "content": prompt}]},
                config=config,
                stream_mode="messages",
            ):
                msg_chunk, _ = chunk
                if not isinstance(msg_chunk, AIMessageChunk):   #跳过ToolMessage
                    continue
                if getattr(msg_chunk, "tool_call_id", None):    #跳过AI发起的tool_call
                    continue
                if msg_chunk.content:
                    full_text += msg_chunk.content
                    placeholder.markdown(full_text)

    # 保存助手回复
    st.session_state["messages"].append({"role": "assistant", "content": full_text})