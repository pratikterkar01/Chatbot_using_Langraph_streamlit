from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages



## define the state
class ChatState(TypedDict):
    content: str
    ai_response: Annotated[list[BaseMessage],add_messages]


## required funtion
def ai_response_creation(state: ChatState):
    response = model.invoke(state['ai_response'])
    return {'ai_response': response.content}



## model initiation
model = ChatOllama(model="llama3.1:8b", temperature=0)
checkpointer = InMemorySaver()
## grah creation
graph = StateGraph(ChatState)

## add node
graph.add_node('response_creation',ai_response_creation)

## add edges
graph.add_edge(START,'response_creation')
graph.add_edge('response_creation',END)


workflow = graph.compile(checkpointer= checkpointer)


def call_graph(user_input:str):
    config1 = {"configurable": {"thread_id": "1"}}
    # below code give the direct output after completely generate the response but we need to deliver message word by word so we
    # implement another method stream provided by the langchian
    #response = workflow.invoke({'ai_response': HumanMessage(content=user_input)},config=config1)
    for message,metadata in workflow.stream({'ai_response': HumanMessage(content=user_input)},config=config1,stream_mode="messages"):
        if message.content:
            print(message.content,end=" ",flush=True)

    #response = workflow.stream({'ai_response': HumanMessage(content=user_input)},config=config1,stream_mode="messages")


    #return {'ai_response': response['ai_response'][-1].content}
    pass

#ai_response = call_graph("is your llm model capable to habdle the codes")
#print(ai_response)
