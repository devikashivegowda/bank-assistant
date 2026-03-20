import streamlit as st
from src.rag_engine import setup_rag_chain

# --- Page Configuration ---
st.set_page_config(
    page_title="PaiKane - Loan Assistant",
    page_icon="🏦",
    layout="centered"
)

# --- App Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True) # Corrected parameter

st.title("🏦 Bank of Maharashtra Loan Assistant")
st.subheader("Your AI-powered guide to every loan products")

# --- Initialize the RAG Chain ---
# We use @st.cache_resource so the vector store and LLM load only once
@st.cache_resource
def load_assistant():
    return setup_rag_chain()

try:
    qa_chain = load_assistant()
except Exception as e:
    st.error(f"Error loading RAG Engine: {e}")
    st.stop()

# --- Chat Interface Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask about interest rates, eligibility, or loan schemes..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            full_response = qa_chain.query(prompt)
            st.markdown(full_response)
            
    # Add assistant message to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Download Chat Button ---
if st.session_state.messages:
    # Prepare the chat history as a string
    chat_history_text = "BANK OF MAHARASHTRA LOAN ASSISTANT - CHAT HISTORY\n"
    chat_history_text += "="*50 + "\n\n"
    
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        chat_history_text += f"{role}: {msg['content']}\n\n"
    
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Download Chat History",
        data=chat_history_text,
        file_name="loan_assistant_chat.txt",
        mime="text/plain"
    )