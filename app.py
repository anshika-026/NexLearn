import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page config
st.set_page_config(
    page_title="Learn-Lynx: AI Study Tutor",
    page_icon="🦁",
    layout="centered"
)

# Title
st.title("🦁 Learn-Lynx: AI Study Tutor")
st.markdown("*Your personal GenAI-powered study partner!*")
st.divider()

# Subject selector
subject = st.selectbox(
    "📚 Select Subject:",
    ["General", "Mathematics", "Physics", "Chemistry", "Biology",
     "Computer Science", "History", "English", "Economics"]
)

# Mode selector
mode = st.radio(
    "🎯 Choose Mode:",
    ["💬 Ask a Question", "📝 Generate Quiz", "📖 Explain a Topic"],
    horizontal=True
)

st.divider()

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if mode == "💬 Ask a Question":
    placeholder = f"Ask me anything about {subject}..."
elif mode == "📝 Generate Quiz":
    placeholder = f"Enter a topic in {subject} to generate a quiz..."
else:
    placeholder = f"Enter a topic in {subject} to get a detailed explanation..."

user_input = st.chat_input(placeholder)

if user_input:
    # Build prompt based on mode
    if mode == "💬 Ask a Question":
        prompt = f"You are a helpful study tutor for {subject}. Answer this question clearly and in simple terms for a student: {user_input}"
    elif mode == "📝 Generate Quiz":
        prompt = f"Generate 5 multiple choice quiz questions about '{user_input}' in {subject}. Format each question with options A, B, C, D and provide the correct answer at the end."
    else:
        prompt = f"Explain the topic '{user_input}' in {subject} in a clear, detailed, and student-friendly way. Include key points, examples, and important formulas if applicable."

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)
            reply = response.text
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **Learn-Lynx** is a GenAI-powered study tutor built with:
    - 🤖 Google Gemini AI
    - 🖥️ Streamlit
    - 🐍 Python
    
    **Features:**
    - Ask subject questions
    - Generate quizzes
    - Get topic explanations
    - Chat history
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("*Built for Gen AI Capstone 2025*")
    