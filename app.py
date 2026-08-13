import streamlit as st
from datetime import datetime
from agent import ask_agent


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="💬",
    layout="wide"
)


# ==================================================
# SIMPLE CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 30px;
        font-weight: 600;
    }

    .subtitle {
        color: #666;
        font-size: 15px;
    }

    .online {
        color: #2e7d32;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("💬 Support")

    st.caption("AI Customer Support Assistant")

    st.divider()

    st.subheader("Quick Questions")

    if st.button(
        "📦 Track an order",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "Where is my order ORD1001?"
        )

    if st.button(
        "↩️ Return policy",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is your return policy?"
        )

    if st.button(
        "💰 Refund policy",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is your refund policy?"
        )

    if st.button(
        "🚚 Shipping policy",
        use_container_width=True
    ):
        st.session_state.quick_question = (
            "What is your shipping policy?"
        )

    st.divider()

    st.subheader("Support Topics")

    st.write("• Orders")
    st.write("• Shipping")
    st.write("• Returns")
    st.write("• Refunds")
    st.write("• Cancellations")

    st.divider()

    if st.button(
        "Clear conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        if "quick_question" in st.session_state:
            del st.session_state.quick_question

        st.rerun()


# ==================================================
# HEADER
# ==================================================

col1, col2 = st.columns([5, 1])

with col1:

    st.markdown(
        '<div class="main-title">'
        '💬 AI Customer Support'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Get help with orders, shipping, returns, refunds, '
        'and cancellations.'
        '</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        '<div class="online">● Online</div>',
        unsafe_allow_html=True
    )


st.divider()


# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(message["content"])

        if "time" in message:

            st.caption(message["time"])


# ==================================================
# GET QUESTION FROM QUICK BUTTON
# ==================================================

quick_question = st.session_state.pop(
    "quick_question",
    None
)


# ==================================================
# GET QUESTION FROM CHAT INPUT
# ==================================================

chat_question = st.chat_input(
    "Ask your question..."
)


# Use quick question if selected
question = quick_question or chat_question


# ==================================================
# PROCESS QUESTION
# ==================================================

if question:

    current_time = datetime.now().strftime(
        "%I:%M %p"
    )


    # ----------------------------------------------
    # USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "time": current_time
        }
    )


    with st.chat_message("user"):

        st.write(question)

        st.caption(current_time)


    # ----------------------------------------------
    # AI RESPONSE
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = ask_agent(question)

                st.write(response)


                # Save response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "time": datetime.now().strftime(
                            "%I:%M %p"
                        )
                    }
                )


            except Exception as e:

                st.error(
                    "Unable to process your request."
                )

                st.caption(
                    f"Error: {e}"
                )