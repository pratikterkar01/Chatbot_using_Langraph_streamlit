import streamlit as st
import chatbot_backend as backend
from langchain_core.messages import BaseMessage,HumanMessage


# session state which not erase when run  once again
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



user_input = st.chat_input('Type here')
if user_input:
    st.session_state['message_history'].append({'role':'user','content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

if user_input is not None:
    with st.chat_message('assistant'):
       config1 = {"configurable": {"thread_id": "1"}}
       ai_response = st.write_stream(message.content for message,metadata in backend.workflow.stream({'ai_response': HumanMessage(content=user_input)},config=config1,stream_mode="messages"))
       st.session_state['message_history'].append({'role': 'assistant', 'content':ai_response})





