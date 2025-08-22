"""Streamlit demo with chat-based approval."""

import time
from datetime import datetime

import streamlit as st

from src import TravelPlannerGraph


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "graph" not in st.session_state:
        st.session_state.graph = TravelPlannerGraph(
            enable_human_loop=True, enable_memory=True
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
    st.markdown("**Chat-based multi-agent system with natural approval workflow**")

    # Chat Interface
    st.subheader("💬 Chat Interface")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Examples below chat
    st.divider()
    st.caption("💡 Try these examples:")
    example_cols = st.columns(2)
    examples = [
        "Plan a 3-day trip to Rome",
        "What's the weather in London?",
        "Find hotels in Tokyo for 2 nights",
        "Search flights to Paris",
        "Confirm booking for Hotel Tokyo, Dec 15-17",
    ]

    # Example buttons
    for i, example in enumerate(examples):
        with example_cols[i % 2]:
            st.button(
                example,
                key=f"btn_{example}",
                on_click=handle_example_click,
                args=(example,),
                use_container_width=True,
            )

    # Chat input at the bottom
    if prompt := st.chat_input("Ask about travel planning...", key="chat_input"):
        # Add user message and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Process with agents
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                start_time = time.time()
                response = st.session_state.graph.chat(
                    prompt, conversation_id=st.session_state.conversation_id
                )
                end_time = time.time()

                # Check if interrupted
                if isinstance(response, dict) and response.get("interrupted"):
                    response_text = f"⏸️ **Booking confirmation required**\n\n*Please respond with 'approve' or 'reject' to continue.*"
                else:
                    response_text = response

            st.write(response_text)

        # Add assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

    # Clear button at the bottom
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_id = f"streamlit_{int(time.time())}"
        st.rerun()


if __name__ == "__main__":
    main()
