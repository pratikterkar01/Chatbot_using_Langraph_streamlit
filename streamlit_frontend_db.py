import streamlit as st
import Langraph_DB_backend as backend
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
import uuid

# -----------------------utility funtion------------------
## return unique thread id for conversation
def generate_thread():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    st.session_state['thread_id'] = generate_thread()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversatin(thread_id):
    conversation = backend.workflow.get_state(config={"configurable": {"thread_id": thread_id}})
    return conversation.values.get('ai_response',[])

# ------------------session state which not erase when run  once again
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = backend.retrive_thread_ids()
add_thread(st.session_state['thread_id'])

# ------------------------ Side bar UI ------------------------------
st.sidebar.title('Chatbot')
if st.sidebar.button("New chat"):
    reset_chat()
st.sidebar.header("Old conversation")
for threads in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(threads)):
        st.session_state['thread_id'] = threads
        messages = load_conversatin(threads)
        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


#--------------------------------------------------------
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



user_input = st.chat_input('Type here')
if user_input:
    st.session_state['message_history'].append({'role':'user','content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):
       def ai_only_stram():
           for message,metadata in backend.workflow.stream({'ai_response': HumanMessage(content=user_input)},config=CONFIG,stream_mode="messages"):
               if isinstance(message, AIMessage):
                   # yield only assistant tokens
                   yield message.content


       #config1 = {"configurable": {"thread_id": st.session_state['thread_id']}}
       ai_response = st.write_stream(ai_only_stram())
    st.session_state['message_history'].append({'role': 'assistant', 'content':ai_response})





