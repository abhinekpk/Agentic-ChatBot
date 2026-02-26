from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot with tool usecase implementation
    """
    def __init__(self,model):
        self.llm=model

    def process(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response using the tool.
        """
        user_input=state["messages"][-1] if state["messages"] else ""
        llm_response=self.llm.invoke(state[{"role":"user","content":user_input}])

        tool_response= f"Tool response for the input: {user_input}"

        return {"messages":[llm_response,tool_response]}
    
    def create_chatbot(self, tools):
        """
        Creates a chatbot node with tool integration.
        """
        
        llm_with_tools_node=self.llm.bind_tools(tools)

        def chatbot_node(state:State) :
            return {"messages":[llm_with_tools_node.invoke(state['messages'])]}
        
        return chatbot_node