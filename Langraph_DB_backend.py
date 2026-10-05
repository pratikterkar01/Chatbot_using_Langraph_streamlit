from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict,Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
import sqlite3


## define the state
class ChatState(TypedDict):
    content: str
    ai_response: Annotated[list[BaseMessage],add_messages]


## required funtion
def ai_response_creation(state: ChatState):
    response = model.invoke(state['ai_response'])
    return {'ai_response': response.content}

## connect with DB
connection = sqlite3.connect(database="chatbot.db",check_same_thread=False)





## model initiation
model = ChatOllama(model="llama3.1:8b", temperature=0)
checkpointer = SqliteSaver(connection)
## grah creation
graph = StateGraph(ChatState)

## add node
graph.add_node('response_creation',ai_response_creation)

## add edges
graph.add_edge(START,'response_creation')
graph.add_edge('response_creation',END)


workflow = graph.compile(checkpointer= checkpointer)

## test
'''CONFIG = {'configurable': {'thread_id': 'thread_id_2'}}

response = workflow.invoke({'ai_response': HumanMessage(content="what is my name ?")},config=CONFIG)
print(response)'''

def retrive_thread_ids():
    thread_id_list = set()
    for checkpoint in checkpointer.list(None):
        thread_id_list.add(checkpoint.config['configurable']['thread_id'])
    return  list(thread_id_list)

'''messages = (workflow.get_state(config={"configurable": {"thread_id": 'thread_id_1'}}))
temp_messages = []
for msg in messages.values.get('ai_response',[]):
    if isinstance(msg, HumanMessage):
        role = 'user'
    else:
        role = 'assistant'
    temp_messages.append({'role': role, 'content': msg.content})

print(temp_messages)'''