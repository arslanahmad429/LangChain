import streamlit as st
from langraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Ask something')

if user_input:
    
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    
    with st.chat_message('Assistant'):
        def response_generator():
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                content = message_chunk.content
                
                if isinstance(content, str) and content:
                    yield content
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            yield item["text"]

       
        ai_message = st.write_stream(response_generator())
        
       
        if isinstance(ai_message, list):
            ai_message = "".join([item.get("text", "") for item in ai_message if isinstance(item, dict)])
        else:
            ai_message = str(ai_message)
            
    
        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})