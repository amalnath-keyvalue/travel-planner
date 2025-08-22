"""Streamlit demo with button-based approval."""

import time

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
    if "awaiting_approval" not in st.session_state:
        st.session_state.awaiting_approval = None


def handle_example_click(text: str):
    """Handle example button click."""
    st.session_state["chat_input"] = text


def handle_approval(approved: bool):
    """Handle booking approval/rejection."""
    st.session_state.graph.chat(
        str(approved), conversation_id=st.session_state.conversation_id
    )
    st.session_state.awaiting_approval = None
    st.rerun()


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Multi-Agent Travel Planner",
        page_icon="🤖",
        layout="wide",
    )

    initialize_session_state()

    st.title("🤖 Multi-Agent Travel Planner")
    st.markdown("**Chat-based multi-agent system with button-based approval workflow**")

    # Examples at top (fixed position)
    st.caption("💡 Try these examples:")
    example_cols = st.columns(2)
    examples = [
        "Plan a 3-day trip to Rome",
        "What's the weather in London?",
        "Find hotels in Tokyo for 2 nights",
        "Search flights to Paris",
        "Book Hotel Tokyo for Dec 15-17",
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

    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Show approval buttons if needed
    if st.session_state.awaiting_approval:
        booking_info = st.session_state.awaiting_approval
        st.info("Please confirm this booking:")

        # Display booking details nicely
        if booking_info["type"] == "accommodation_booking":
            st.markdown(
                f"""
                🏨 **Accommodation Booking**
                - Hotel: {booking_info['accommodation_name']}
                - Location: {booking_info['destination']}
                - Check-in: {booking_info['check_in']}
                - Check-out: {booking_info['check_out']}
                - Guest: {booking_info['guest_name']}
                - Payment: {booking_info['payment_method']}
                """
            )
        else:  # flight_booking
            st.markdown(
                f"""
                ✈️ **Flight Booking**
                - Airline: {booking_info['airline']}
                - Route: {booking_info['route']}
                - Date: {booking_info['departure_date']}
                - Passenger: {booking_info['passenger_name']}
                - Payment: {booking_info['payment_method']}
                """
            )

        # Approval buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "✅ Confirm Booking",
                on_click=handle_approval,
                args=(True,),
                type="primary",
                use_container_width=True,
            )
        with col2:
            st.button(
                "❌ Cancel Booking",
                on_click=handle_approval,
                args=(False,),
                use_container_width=True,
            )

    # Chat input
    if prompt := st.chat_input("Ask about travel planning...", key="chat_input"):
        # Add user message and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Process with agents
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    response = st.session_state.graph.chat(
                        prompt, conversation_id=st.session_state.conversation_id
                    )
                    # Check if interrupted
                    if isinstance(response, dict) and response.get("interrupted"):
                        st.session_state.awaiting_approval = response.get("data", {})
                        response_text = "⏸️ **Booking confirmation required**\n\nPlease use the buttons above to confirm or cancel this booking."
                    else:
                        response_text = response
                except Exception as e:
                    response_text = f"❌ Error: {str(e)}"

            st.write(response_text)

        # Add assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

    # Clear button (only show if there are messages)
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_id = f"streamlit_{int(time.time())}"
            st.session_state.awaiting_approval = None
            st.rerun()


if __name__ == "__main__":
    main()
