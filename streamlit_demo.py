"""Streamlit app to view actual agent interactions."""

import streamlit as st
from langchain_core.messages import HumanMessage

from src import TravelSupervisorGraph


def show_agent_trace(messages):
    """Show the actual agent conversation trace."""
    st.markdown("### 🔍 Agent Trace")

    for i, msg in enumerate(messages):
        if hasattr(msg, "name") and msg.name:
            # Agent message
            agent_name = msg.name.replace("_", " ").title()
            with st.expander(f"🤖 {agent_name}", expanded=(i < 3)):
                st.write(msg.content)
        elif hasattr(msg, "tool_calls") and msg.tool_calls:
            # Tool calls
            with st.expander(f"🔧 Tool Calls", expanded=True):
                for tool_call in msg.tool_calls:
                    st.code(f"Tool: {tool_call['name']}")


def main():
    """Main app."""
    st.set_page_config(page_title="Agent Viewer", page_icon="🔍", layout="wide")

    st.title("🔍 Multi-Agent Interaction Viewer")
    st.caption("See actual LangGraph agent conversations")

    # Initialize
    if "system" not in st.session_state:
        st.session_state.system = TravelSupervisorGraph()

    # Input
    query = st.text_input("Query:", placeholder="Plan a 3-day trip to Tokyo")

    if query:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 💬 User Query")
            st.write(query)

            st.markdown("### 🤖 Final Response")
            with st.spinner("Processing..."):
                # Get the full graph execution
                result = st.session_state.system.graph.invoke(
                    {"messages": [HumanMessage(content=query)]}
                )

                # Extract final response
                final_response = "No response generated"
                for msg in reversed(result["messages"]):
                    if hasattr(msg, "name") and msg.name in [
                        "search_agent",
                        "planning_agent",
                        "booking_agent",
                    ]:
                        final_response = msg.content
                        break

                st.write(final_response)

        with col2:
            # Show the actual agent interactions
            show_agent_trace(result["messages"])


if __name__ == "__main__":
    main()
