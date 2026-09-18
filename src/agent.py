from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
import sqlite3
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from tools.__init__ import get_all_tools

load_dotenv()

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

def init_model():
    model = init_chat_model(
        model = os.getenv("Model"),
        api_key = os.getenv("API_KEY"),
        base_url = os.getenv("Base_URL")
    )
    return model

def init_agent():
    agent = create_agent(
        model = init_model(),
        tools = get_all_tools(),
        system_prompt = os.getenv("SYSTEM_PROMPT"),
        checkpointer = checkpointer,
    )
    return agent