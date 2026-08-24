import streamlit as st
from langraph_backend import chatbot ,  retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# '''''''''''''''''''''''''Generate Thread ID ''''''''''''''''''''''''''''''''
def generate_thread_id():
    return uuid.uuid4()

# ''''''''''''''''''''''''''''Reset Chat''''''''''''''''''''''''''''''
def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

# '''''''''''''''''''''''''''''''Add thread'''''''''''''''''''''''''''''''
def add_thread(thread_id):
    if 'chat_threads' not in st.session_state:
        st.session_state['chat_threads'] = retrieve_all_threads()
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# ''''''''''''''''''''''''''''Load Conversation (Bulletproof)''''''''''''''''''''''''''''''''''
def load_conversation(thread_id):
    try:
        state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
        if state:
            # Check for modern StateSnapshot .values structure
            if hasattr(state, 'values') and isinstance(state.values, dict):
                return state.values.get('messages', [])
            # Fallback if state is returned as a dict mapping
            elif isinstance(state, dict):
                values = state.get('values', {})
                if isinstance(values, dict):
                    return values.get('messages', [])
    except Exception:
        pass
    return []

# '''''''''''''''''''''''''' Session Setup '''''''''''''''''''''''''''
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])    

# ''''''''''''''''''''''''''Sidebar UI'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()
    st.rerun()

st.sidebar.title('My Conversations')

# Loop through threads safely using a copy of the list
for tid in list(st.session_state['chat_threads'][::-1]):
    short_label = f"Chat {str(tid)[:8]}"
    if st.sidebar.button(short_label, key=str(tid)):
        st.session_state['thread_id'] = tid
        messages = load_conversation(tid)

        temp_messages = []
        for message in messages:
            raw_content = message.content
            # Safely parse Gemini content list blocks into standard strings
            if isinstance(raw_content, list):
                clean_text = "".join([item.get("text", "") for item in raw_content if isinstance(item, dict)])
            else:
                clean_text = str(raw_content)

            if isinstance(message, HumanMessage):
                temp_messages.append({'role': 'user', 'content': clean_text})
            else:
                temp_messages.append({'role': 'assistant', 'content': clean_text})
                
        st.session_state['message_history'] = temp_messages
        st.rerun()

# Dynamic config mapping for active chat thread
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

# ''''''''''''''''''''''''''' Main Chat UI Display ''''''''''''''''''''''''''''''''''''''''''''''
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
        
        # Format safeguard check
        if isinstance(ai_message, list):
            ai_message = "".join([item.get("text", "") for item in ai_message if isinstance(item, dict)])
        else:
            ai_message = str(ai_message)
            
        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})