from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tools import get_tools , create_tool_node
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_node=BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds a chatbot graph with tools using LangGraph.
        This method initializes a chatbot node with tool integration and incorporates it into the graph. 
        The chatbot node is designated as both the entry and exit point of the graph, allowing for enhanced interactions with tool capabilities.
        """
        ## Define tools and tool nodes
        tools = get_tools()
        tool_node = create_tool_node(tools)

        ## define LLM
        llm=self.llm

        ## Define chatbot node with tools
        chatbot_with_tool_node=ChatbotWithToolNode(llm)
        chatbot_node=chatbot_with_tool_node.create_chatbot(tools)
        ## Add Nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)  

        ## Define normal and conditional edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")

    def ai_news_build_graph(self):
        """
        Placeholder for AI News graph build method.
        This method is intended to build a graph for an AI news use case. 
        The implementation will be added in the future to incorporate nodes and edges specific to the AI news functionality.
        """
        
        ai_news_node=AINewsNode(self.llm)
        fetch_news_node=ai_news_node.fetch_news
        summarize_news_node=ai_news_node.summarize_news 
        save_news_node=ai_news_node.save_news

        ## Define nodes
        self.graph_builder.add_node("fetch_news",fetch_news_node)
        self.graph_builder.add_node("summarize_news",summarize_news_node)
        self.graph_builder.add_node("save_news",save_news_node)

        ## Define edges
        self.graph_builder.add_edge(START,"fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_news")
        self.graph_builder.add_edge("save_news",END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        if usecase == "Chatbot with Tools":
            self.chatbot_with_tools_build_graph()
        
        if usecase == "AI News":
            self.ai_news_build_graph()

        return self.graph_builder.compile()

    