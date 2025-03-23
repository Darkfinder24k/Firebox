import streamlit as st
import google.generativeai as genai
import time

# Secure API Key Handling
genai.configure(api_key="AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4")

# User Subscription Database (Demo - Replace with Firebase/Database)
premium_users = {"kushagra@gmail.com", "premium_user@example.com"}  # Add premium users here

# Streamlit Page Config (Must be the first command)
st.set_page_config(page_title="Firebox AI", layout="wide")

# User Authentication
user_email = st.sidebar.text_input("Enter your Email:")
is_premium = user_email in premium_users

# AI Model Selection
class FireboxAI:
    def __init__(self, is_premium, max_tokens=2048):
        model_name = "gemini-2.0-flash" if is_premium else "gemini-1.5-pro"
        self.model = genai.GenerativeModel(model_name, generation_config={"max_output_tokens": max_tokens})

    def ask_firebox(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else "Error: No response."
        except Exception:
            return "Error: Firebox AI encountered an issue. Please try again later."

# Initialize Firebox AI
ai = FireboxAI(is_premium)

# Firebox Premium Promotion Popup (Shows on Page Load)
if "show_premium_popup" not in st.session_state:
    st.session_state.show_premium_popup = True

if st.session_state.show_premium_popup:
    st.warning("🔥 Upgrade to Firebox Premium for ultra-fast responses, premium UI, and more features!")
    st.session_state.show_premium_popup = False

# UI Differences for Premium Users
if is_premium:
    st.sidebar.title("🔥 Firebox AI - Very Pro Premium")
    st.title("🚀 Firebox AI Premium Assistant")
else:
    st.sidebar.title("🔥 Firebox AI - Free")
    st.title("Firebox AI Assistant")

# Memory Slider
memory_depth = st.sidebar.slider("Memory Depth", min_value=1, max_value=10, value=5)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Text Input Query
txt_query = st.chat_input("Ask Firebox AI...")
if txt_query:
    with st.chat_message("user"):
        st.markdown(txt_query)
    with st.spinner("Generating response..."):
        firebox_response = ai.ask_firebox(txt_query)
        if not is_premium:
            time.sleep(3)  # Simulating slower response generation for free users
    with st.chat_message("assistant"):
        st.markdown(firebox_response)
    st.session_state.messages.append({"role": "user", "content": txt_query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show Firebox Premium Promotion Every 3 Minutes
if "last_premium_prompt" not in st.session_state:
    st.session_state.last_premium_prompt = time.time()

if time.time() - st.session_state.last_premium_prompt > 180:
    st.sidebar.warning("🔥 Upgrade to Firebox Premium for ultra-fast responses, premium UI, and more features!")
    st.session_state.last_premium_prompt = time.time()

# Hide Streamlit Branding, Fork Button, and Footer
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
