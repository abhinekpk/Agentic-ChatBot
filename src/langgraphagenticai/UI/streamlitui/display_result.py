import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def _parse_tool_payload(self, content):
        if isinstance(content, (list, dict)):
            return content

        if not isinstance(content, str):
            return content

        try:
            return json.loads(content)
        except Exception:
            return content

    def _render_clean_tool_response(self, content):
        payload = self._parse_tool_payload(content)

        with st.chat_message("assistant"):
            with st.expander("Tool Response", expanded=False):
                if (
                    isinstance(payload, list)
                    and payload
                    and all(isinstance(item, dict) for item in payload)
                ):
                    for index, item in enumerate(payload, start=1):
                        title = item.get("title", f"Result {index}")
                        url = item.get("url")
                        snippet = item.get("content") or item.get("snippet") or ""
                        score = item.get("score")

                        st.markdown(f"**{index}. {title}**")
                        if url:
                            st.markdown(f"[Source]({url})")
                        if score is not None:
                            st.caption(f"Score: {score}")
                        if snippet:
                            st.write(snippet)
                        if index < len(payload):
                            st.divider()
                elif isinstance(payload, (dict, list)):
                    st.json(payload)
                else:
                    st.write(payload)

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
        
        elif usecase=="Chatbot with Tools":
            
            intial_state={"messages":[user_message]}
            res =graph.invoke(intial_state)
            for message in res["messages"]:
                if type(message)==HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)==ToolMessage:
                    self._render_clean_tool_response(message.content)
                elif type(message)==AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
