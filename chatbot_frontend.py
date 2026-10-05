import streamlit as st
import chatbot_backend as backend

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
    ai_response = backend.call_graph(user_input)
    if ai_response:
        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_response['ai_response']})
        with st.chat_message('assistant'):
            st.text(ai_response['ai_response'])




