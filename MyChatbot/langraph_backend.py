from langgraph.graph import StateGraph , START , END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash')
class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]
def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages':[response]}
connector = sqlite3.connect(database='chatbot.db', check_same_thread= False)
checkpointer = SqliteSaver(connector)

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node" ,END)
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()  # Using a set as requested
    try:
        # checkpointer.list(None) fetches checkpoints
        checkpoints = checkpointer.list(None)
        if checkpoints:
            for checkpoint in checkpoints:
                if checkpoint and checkpoint.config and 'configurable' in checkpoint.config:
                    tid = checkpoint.config['configurable'].get('thread_id')
                    if tid:
                        all_threads.add(tid)
    except Exception:
        pass
    
    return list(all_threads)