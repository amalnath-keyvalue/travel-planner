"""Streamlit demo with multi-agent communication."""

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
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None


def add_log(step: str, details: str = ""):
    """Add log entry with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {step}")
    if details:
        st.session_state.logs.append(f"           {details}")


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Multi-Agent Travel Planner",
        page_icon="🤖",
        layout="wide",
    )

    initialize_session_state()

    st.title("🤖 Multi-Agent Travel Planner")
    st.markdown(
        "**Supervisor-based multi-agent system with human approval for bookings**"
    )

    # Create columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 Chat Interface")

        # Handle pending approval
        if st.session_state.pending_approval:
            st.warning("⏸️ Workflow paused - approval required")

            interrupt_info = st.session_state.pending_approval
            st.info(f"**Next:** {interrupt_info.get('next_step', 'booking_agent')}")
            st.write(f"**Request:** {interrupt_info.get('user_request', 'Unknown')}")

            col_approve, col_reject = st.columns(2)
            with col_approve:
                if st.button("✅ Approve", use_container_width=True):
                    add_log("👤 Human", "Approved")

                    with st.spinner("Continuing..."):
                        response = st.session_state.graph.approve_and_continue(
                            conversation_id=st.session_state.conversation_id
                        )

                    add_log("▶️ Resumed", "Workflow continued")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    st.session_state.pending_approval = None
                    st.rerun()

            with col_reject:
                if st.button("❌ Reject", use_container_width=True):
                    add_log("👤 Human", "Rejected")

                    response = st.session_state.graph.reject_and_stop(
                        conversation_id=st.session_state.conversation_id
                    )

                    add_log("❌ Stopped", "Workflow ended")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    st.session_state.pending_approval = None
                    st.rerun()

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if not st.session_state.pending_approval:
            if prompt := st.chat_input("Ask about travel planning..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

                # Clear logs
                st.session_state.logs = []

                # Process with agents
                with st.chat_message("assistant"):
                    with st.spinner("Processing..."):
                        add_log("📨 Input", f"'{prompt}'")
                        add_log("🧠 Supervisor", "Analyzing")

                        start_time = time.time()
                        response = st.session_state.graph.chat(
                            prompt, conversation_id=st.session_state.conversation_id
                        )
                        end_time = time.time()

                        # Check if interrupted
                        if isinstance(response, dict) and response.get("interrupted"):
                            add_log("⏸️ Interrupt", "Paused for approval")
                            st.session_state.pending_approval = response
                            st.rerun()
                        else:
                            add_log("✅ Complete", f"({end_time - start_time:.1f}s)")

                    st.write(response)

                # Add assistant message
                if not isinstance(response, dict):
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

    with col2:
        st.subheader("📊 Communication Logs")

        # Display logs
        if st.session_state.logs:
            for log_entry in st.session_state.logs:
                if log_entry.startswith("["):
                    st.code(log_entry, language=None)
                else:
                    st.text(log_entry)
        else:
            st.info("Start a conversation to see logs")

        # Examples
        st.subheader("💡 Examples")

        examples = [
            "Plan a 3-day trip to Rome",
            "What's the weather in London?",
            "Book a hotel in Tokyo",
            "Reserve a flight to Paris",
        ]

        for example in examples:
            if st.button(example, key=f"btn_{example}", use_container_width=True):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": example})

                # Clear logs
                st.session_state.logs = []

                # Process with agents
                add_log("📨 Input", f"'{example}'")
                add_log("🧠 Supervisor", "Analyzing")

                start_time = time.time()
                response = st.session_state.graph.chat(
                    example, conversation_id=st.session_state.conversation_id
                )
                end_time = time.time()

                # Check if interrupted
                if isinstance(response, dict) and response.get("interrupted"):
                    add_log("⏸️ Interrupt", "Paused for approval")
                    st.session_state.pending_approval = response
                else:
                    add_log("✅ Complete", f"({end_time - start_time:.1f}s)")
                    # Add assistant message
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

                st.rerun()

        # Info
        st.subheader("ℹ️ System Info")
        st.text("• Planning: Supervisor handles directly")
        st.text("• Search: Delegates to search agent")
        st.text("• Booking: Requires human approval")

        # Clear
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.logs = []
            st.session_state.pending_approval = None
            st.session_state.conversation_id = f"streamlit_{int(time.time())}"
            st.rerun()


if __name__ == "__main__":
    main()
