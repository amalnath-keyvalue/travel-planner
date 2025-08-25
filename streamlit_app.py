"""Streamlit demo for multi-agent travel planner."""

import time

import streamlit as st

from src import TravelPlannerGraph
from src.memory import get_session_memories


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "graph" not in st.session_state:
        st.session_state.graph = TravelPlannerGraph()
    if "chat_tabs" not in st.session_state:
        st.session_state.chat_tabs = {
            "current_session": {
                "id": f"session_{int(time.time())}",
                "messages": [],
                "title": "Session 1",
            }
        }
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "current_session"
    if "pending_interrupt" not in st.session_state:
        st.session_state.pending_interrupt = None


def handle_example_click(text: str):
    """Handle example button click."""
    st.session_state[f"chat_input_{st.session_state.active_tab}"] = text


def display_memories(session_id: str):
    memories = get_session_memories(session_id)

    if not any(memories.values()):
        return

    with st.expander("🧠 Session Memories", expanded=False):
        if memories["booking"]:
            st.write("🏨 **Bookings:**")
            for memory in memories["booking"]:
                st.write(f"• {memory.content}")

        if memories["long_term"]:
            st.write("💾 **Long-term Memories:**")
            for memory in memories["long_term"]:
                importance = memory.metadata.get("importance", "medium")
                tags = memory.metadata.get("tags", [])
                tag_str = f" [{', '.join(tags)}]" if tags else ""
                st.write(f"• {memory.content}{tag_str} ({importance})")


def render_chat_interface(session_id: str, tab_data: dict):
    """Render chat interface for a single session."""
    for message in tab_data["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input(
        "Ask about travel planning...",
        key=f"chat_input_{session_id}",
    ):
        tab_data["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    response = st.session_state.graph.chat(
                        prompt,
                        conversation_id=tab_data["id"],
                    )

                    if (
                        isinstance(response, dict)
                        and response.get("type") == "interrupt"
                    ):
                        st.session_state.pending_interrupt = response
                        st.session_state.active_tab = session_id
                        st.rerun()
                    else:
                        st.write(response)
                        tab_data["messages"].append(
                            {"role": "assistant", "content": response}
                        )

                except Exception as e:
                    response_text = f"❌ Error: {str(e)}"
                    st.write(response_text)
                    tab_data["messages"].append(
                        {"role": "assistant", "content": response_text}
                    )


def main():
    st.set_page_config(
        page_title="Multi-Agent Travel Planner",
        page_icon="🤖",
        layout="wide",
    )

    if "graph" not in st.session_state:
        st.session_state.graph = TravelPlannerGraph()

    if "chat_tabs" not in st.session_state:
        st.session_state.chat_tabs = {
            "current_session": {
                "id": "current_session",
                "messages": [],
                "title": "Session 1",
            }
        }

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "current_session"

    if "pending_interrupt" not in st.session_state:
        st.session_state.pending_interrupt = None

    st.title("🤖 Multi-Agent Travel Planner")
    st.markdown("**Session-based multi-agent system using Supervisor pattern**")

    if len(st.session_state.chat_tabs) > 1:
        tab_names = [
            tab_data["title"] for tab_data in st.session_state.chat_tabs.values()
        ]
        selected_tab = st.tabs(tab_names)

        for i, (tab_id, tab_data) in enumerate(st.session_state.chat_tabs.items()):
            with selected_tab[i]:
                st.subheader(f"💬 {tab_data['title']}")
                display_memories(tab_data["id"])
                render_chat_interface(tab_id, tab_data)
    else:
        st.subheader(
            f"💬 {st.session_state.chat_tabs[st.session_state.active_tab]['title']}"
        )
        display_memories(st.session_state.active_tab)
        render_chat_interface(
            st.session_state.active_tab,
            st.session_state.chat_tabs[st.session_state.active_tab],
        )

    if st.session_state.pending_interrupt:
        st.divider()
        st.warning("⚠️ **Human approval required for this action.**")

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✅ Approve", type="secondary", use_container_width=True):
                with st.spinner("Processing approval..."):
                    response = st.session_state.graph.chat(
                        "",
                        conversation_id=st.session_state.chat_tabs[
                            st.session_state.active_tab
                        ]["id"],
                        is_approved=True,
                    )
                    st.session_state.chat_tabs[st.session_state.active_tab][
                        "messages"
                    ].append({"role": "assistant", "content": response})
                    st.session_state.pending_interrupt = None
                    st.success("✅ Action approved successfully!")
                    st.rerun()

        with col2:
            if st.button("❌ Reject", type="secondary"):
                with st.spinner("Processing rejection..."):
                    response = st.session_state.graph.chat(
                        "",
                        conversation_id=st.session_state.chat_tabs[
                            st.session_state.active_tab
                        ]["id"],
                        is_approved=False,
                    )
                    st.session_state.chat_tabs[st.session_state.active_tab][
                        "messages"
                    ].append({"role": "assistant", "content": response})
                    st.session_state.pending_interrupt = None
                    st.error("❌ Action rejected.")
                    st.rerun()

        with col3:
            action_data = st.session_state.pending_interrupt.get("data", {})
            if action_data:
                if action_data.get("display_name"):
                    st.write(f"**{action_data['display_name']}**")

                tool_input = action_data.get("tool_input", {})
                if tool_input:
                    for key, value in tool_input.items():
                        if value:
                            readable_key = key.replace("_", " ").title()
                            st.write(f"• **{readable_key}:** {value}")

    st.sidebar.header("🔗 Graph Structure")
    try:
        mermaid_png = st.session_state.graph.graph.get_graph().draw_mermaid_png()
        st.sidebar.image(mermaid_png, use_container_width=True)
    except Exception as e:
        st.sidebar.error(f"Failed to render graph: {e}")

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
            key=f"example_{example}",
            on_click=handle_example_click,
            type="tertiary",
            args=(example,),
            use_container_width=True,
        )

    st.sidebar.divider()
    if st.sidebar.button("🆕 New Session", type="secondary", use_container_width=True):
        new_tab_id = f"session_{int(time.time())}"
        st.session_state.chat_tabs[new_tab_id] = {
            "id": new_tab_id,
            "messages": [],
            "title": f"Session {len(st.session_state.chat_tabs) + 1}",
        }
        st.session_state.active_tab = new_tab_id
        st.rerun()


if __name__ == "__main__":
    main()
