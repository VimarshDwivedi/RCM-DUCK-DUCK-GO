import streamlit as st
from search import search_duckduckgo
from utils import generate_context
from llm_model import get_llm_response
import time
import random

# Page configuration with custom theme colors
st.set_page_config(
    page_title="RCM Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .subheader {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-top: 1.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .result-container {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin: 1rem 0;
        border-left: 5px solid #1E88E5;
    }
    .source-item {
        margin-bottom: 0.8rem;
        padding: 0.8rem;
        border-radius: 5px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    .query-box {
        border: 2px solid #1E88E5;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #0D47A1;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with app info
with st.sidebar:
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/master/frontend/public/favicon.png", width=100)
    st.header("About RCM Assistant")
    st.write("This intelligent assistant helps you find and understand information by searching the web and generating comprehensive responses.")
    
    st.markdown("---")
    st.subheader("Features")
    st.markdown("• Web search integration")
    st.markdown("• Context-aware responses")
    st.markdown("• Source attribution")
    st.markdown("• Simple, user-friendly interface")
    
    st.markdown("---")
    st.markdown("### Made with ❤️ by")
    st.markdown("## Vimarsh Dwivedi")

# Main content
st.markdown('<h1 class="main-header">🧠 RCM Assistant</h1>', unsafe_allow_html=True)
st.markdown("Ask any question and get comprehensive answers with reliable sources.")

# Search query input with a nice container
st.markdown('<div class="query-box">', unsafe_allow_html=True)
query = st.text_input("What would you like to know?", placeholder="Enter your question here...")
col1, col2 = st.columns([4, 1])
with col1:
    search_button = st.button("🔍 Search", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'results' not in st.session_state:
    st.session_state.results = []
if 'answer' not in st.session_state:
    st.session_state.answer = ""

# Clear results when clear button is clicked
if clear_button:
    st.session_state.query = ""
    st.session_state.results = []
    st.session_state.answer = ""
    st.experimental_rerun()

# Search processing
if search_button and query:
    st.session_state.query = query
    
    # Progress bar for better UX
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate search progress
    status_text.text("Searching the web...")
    for i in range(40):
        progress_bar.progress(i + 1)
        time.sleep(0.01)
    
    # Actual search
    results = search_duckduckgo(query)
    
    if not results:
        progress_bar.empty()
        status_text.empty()
        st.error("No results found. Please try a different query.")
    else:
        # Continue progress for context generation
        status_text.text("Generating context from search results...")
        for i in range(40, 70):
            progress_bar.progress(i + 1)
            time.sleep(0.01)
            
        context = generate_context(results)
        
        # Continue progress for LLM response
        status_text.text("Crafting your answer...")
        for i in range(70, 100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)
            
        answer = get_llm_response(context, query)
        
        # Store results
        st.session_state.results = results
        st.session_state.answer = answer
        
        # Clear progress elements
        progress_bar.empty()
        status_text.empty()

# Display results if available
if st.session_state.query and st.session_state.answer:
    st.markdown('<h2 class="subheader">📝 Answer</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.markdown(st.session_state.answer)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display sources with better formatting
    st.markdown('<h2 class="subheader">🔗 Sources</h2>', unsafe_allow_html=True)
    
    for i, result in enumerate(st.session_state.results, 1):
        with st.container():
            st.markdown(f'<div class="source-item">', unsafe_allow_html=True)
            st.markdown(f"**{i}. [{result['title']}]({result['href']})**")
            st.markdown(f"{result['body']}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Add feedback option
    st.markdown('<h2 class="subheader">📊 Feedback</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("👍 Helpful"):
            st.success("Thank you for your feedback!")
    with col2:
        if st.button("👎 Not Helpful"):
            st.info("Sorry to hear that. We'll work to improve our responses.")
    with col3:
        if st.button("📝 Report Issue"):
            st.warning("Issue reported. Thank you for helping us improve!")

# Footer with attribution
st.markdown("""
<div class="footer">
    <p>RCM Assistant v1.0 | Developed by <b>Vimarsh Dwivedi</b> | © 2025</p>
</div>
""", unsafe_allow_html=True)