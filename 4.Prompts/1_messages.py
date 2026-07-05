from langchain_core.messages import SystemMessage , AIMessage , HumanMessage 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-3.5-flash")
messages = [
    SystemMessage(content="You are An Applied AI Engineer"),
    HumanMessage(content="Tell Me About LangChain")
]
result = model.invoke(messages)
messages.append(AIMessage(content=result.content))
print(messages)
#print(result.content)