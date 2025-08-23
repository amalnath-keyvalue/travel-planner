"""Streamlit demo for multi-agent travel planner."""

import time

import streamlit as st

from src import TravelPlannerGraph


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "graph" not in st.session_state:
        st.session_state.graph = TravelPlannerGraph(
            enable_memory=True,
        )
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = f"streamlit_{int(time.time())}"
    if "messages" not in st.session_state:
        st.session_state.messages = []


def handle_example_click(text: str):
    """Handle example button click."""
    st.session_state["chat_input"] = text


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Multi-Agent Travel Planner",
        page_icon="🤖",
        layout="wide",
    )

    initialize_session_state()

    st.title("🤖 Multi-Agent Travel Planner")
    st.markdown("**Chat-based multi-agent system using Supervisor pattern**")

    # Display the graph structure
    st.sidebar.header("🔗 Graph Structure")
    try:
        mermaid_png = st.session_state.graph.graph.get_graph().draw_mermaid_png()
        st.sidebar.image(mermaid_png, caption="LangGraph Structure")
    except Exception as e:
        st.sidebar.error(f"Could not display graph: {e}")

    # Examples in sidebar
    st.sidebar.header("💡 Try these examples:")
    examples = [
        "Plan a 3-day trip to Rome",
        "What's the weather in London?",
        "Find hotels in Tokyo for 2 nights",
        "Search flights to Paris",
        "Book a hotel in Tokyo for Dec 15-17",
    ]

    for example in examples:
        st.sidebar.button(
            example,
            key=f"btn_{example}",
            on_click=handle_example_click,
            args=(example,),
            use_container_width=True,
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask about travel planning...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    response = st.session_state.graph.chat(
                        prompt, conversation_id=st.session_state.conversation_id
                    )
                    response_text = response
                except Exception as e:
                    response_text = f"❌ Error: {str(e)}"

            st.write(response_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

    if st.session_state.messages:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_id = f"streamlit_{int(time.time())}"
            st.rerun()


if __name__ == "__main__":
    main()
