import os
from dotenv import load_dotenv
from typing import TypedDict, List

from fastapi import FastAPI
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# ---------------- Setup ----------------
load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
# MODEL = "gemini-2.5-flash"


llm = ChatGoogleGenerativeAI(
    model=MODEL,
    api_key=API_KEY,
    temperature=0.0
)

app = FastAPI()

# ---------------- State ----------------
class ChatState(TypedDict):
    user_input: str
    chat_history: List
    llm_response: str

# In-memory session memory (simple)
MEMORY = {"chat_history": []}

# ---------------- Nodes ----------------
def llm_node(state: ChatState):
    messages = state["chat_history"] + [
        HumanMessage(content=state["user_input"])
    ]
    response = llm.invoke(messages)
    return {"llm_response": response.content}

def memory_node(state: ChatState):
    updated_history = state["chat_history"] + [
        HumanMessage(content=state["user_input"]),
        AIMessage(content=state["llm_response"])
    ]
    return {"chat_history": updated_history}

# ---------------- Graph ----------------
graph = StateGraph(ChatState)
graph.add_node("llm", llm_node)
graph.add_node("memory", memory_node)

graph.set_entry_point("llm")
graph.add_edge("llm", "memory")
graph.add_edge("memory", END)

chatbot = graph.compile()

# ---------------- API ----------------
@app.post("/chat")
def chat(message: str):
    global MEMORY
    result = chatbot.invoke({
        "user_input": message,
        "chat_history": MEMORY["chat_history"]
    })
    MEMORY["chat_history"] = result["chat_history"]
    return {"response": result["llm_response"]}

@app.get("/")
def health():
    return {"status": "LangGraph Chatbot is running"}
