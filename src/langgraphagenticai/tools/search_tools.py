from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Initializes and returns a list of tools for the agent.
    Currently includes the Tavily Search Tool for web search capabilities.
    """
    tools = [TavilySearchResults(max_results=3)]
    return tools

def create_tool_node(tools):
    """
    Creates ToolNode instances for each tool in the provided list.
    
    Args:
        tools (list): A list of tool instances to be converted into ToolNodes.
    
    Returns:
        list: A list of ToolNode instances corresponding to the input tools.
    """
    return ToolNode(tools=tools)