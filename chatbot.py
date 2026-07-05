# Use the Chat class
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# Use the Chat class with the correct model name
model = ChatGoogleGenerativeAI(model='gemini-3.5-flash')
chat_history = []

while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        break
    
    chat_history.append(HumanMessage(content=user_input))
    
    # This works because ChatGoogleGenerativeAI accepts the list
    result = model.invoke(chat_history)
    
    # This works because result is an AIMessage object
    Response = result.content 
    
    chat_history.append(AIMessage(content=Response))
    print(f'Bot: {Response}')
print(chat_history)