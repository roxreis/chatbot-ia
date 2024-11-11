import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from .database import VectorDatabase
from .utils import get_embedding, is_factual_statement
from dotenv import load_dotenv
from typing import TypedDict, List


class StateType(TypedDict):
    user_input: str
    similar_texts: List[str]
    response: str
    final_response: str


class Chatbot:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"))
        self.db = VectorDatabase()
        self.graph = self.create_graph()

    def create_graph(self):
        workflow = StateGraph(StateType)

        workflow.add_node("process_input", self.process_input)
        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("update_knowledge", self.update_knowledge)

        workflow.set_entry_point("process_input")
        workflow.add_edge("process_input", "generate_response")
        workflow.add_edge("generate_response", "update_knowledge")
        workflow.add_edge("update_knowledge", END)

        return workflow.compile()

    def process_input(self, state):
        user_input = state["user_input"]
        embedding = get_embedding(user_input)
        similar_texts = self.db.search_similar(embedding)
        return {"user_input": user_input, "similar_texts": similar_texts}

    def generate_response(self, state):
        user_input = state["user_input"]
        similar_texts = state["similar_texts"]
        context = "\n".join(similar_texts)
        messages = [HumanMessage(content=f"Context: {context}\nUser: {user_input}")]
        response = self.llm.invoke(messages)
        return {"response": response.content, "user_input": user_input}

    def update_knowledge(self, state):
        user_input = state["user_input"]
        if is_factual_statement(user_input):
            embedding = get_embedding(user_input)
            self.db.store_embedding(user_input, embedding)
        return {"final_response": state["response"]}

    def chat(self, user_input):
        result = self.graph.invoke({"user_input": user_input})
        return result["final_response"]
