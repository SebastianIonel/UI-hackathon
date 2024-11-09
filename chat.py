import streamlit as st

def send_message():
    user_input = st.session_state["text_input_for_chat"]
    if user_input:
        st.session_state["chat_history"].append(f"You: {user_input}")
        st.session_state["chat_history"].append(f"ChatGPT: Your message '{user_input}' was received!")
        st.session_state["input"] = ""  # Clear the input field after sending

def show_chatbox():
    # Initialize session state for storing chat messages if not already initialized
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # Display chat box title
    st.markdown("<h3 style='text-align: center;'>Chat Box</h3>", unsafe_allow_html=True)

    # Placeholder for chat history, placed above the input box
    chat_history_placeholder = st.empty()    

    # User input and send button
    user_input = st.text_input("Start conversation", key="text_input_for_chat", autocomplete="off")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if (st.button("Send") or user_input):
            send_message()

    with col2:
        if st.button("Clear History"):
            # Clear the chat history after the animation
            st.session_state["chat_history"] = []

    # Render the chat history in the placeholder
    with chat_history_placeholder.container():
        for message in st.session_state["chat_history"]:
            st.markdown(f"<div style='text-align: left; color: black;'>{message}</div>", unsafe_allow_html=True)