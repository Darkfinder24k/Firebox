import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Set page config FIRST
st.set_page_config(page_title="Firebox AI", layout="wide")

# Secure API Key Handling
genai.configure(api_key="AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4")

# User Subscription Database (Demo - Replace with Firebase/Database)
premium_users = {"kushagra@gmail.com", "premium_user@example.com"}  # Add premium users here

# User Authentication
user_email = st.sidebar.text_input("Enter your Email:")
is_premium = user_email in premium_users

# AI Model Selection
class FireboxAI:
    def __init__(self, is_premium, max_tokens=2048):
        model_name = "gemini-pro" if is_premium else "gemini-2.0-flash"
        self.model = genai.GenerativeModel(model_name, generation_config={"max_output_tokens": max_tokens})

    def ask_firebox(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            output = response.text if response else "Error: No response."
            return output
        except Exception as e:
            st.error(f"Error: Firebox AI encountered an issue - {str(e)}")
            return "An error occurred. Please try again later."

# Initialize Firebox AI
ai = FireboxAI(is_premium)

# Streamlit UI
st.sidebar.title("🔥 Firebox AI - Very Pro Premium" if is_premium else "🔥 Firebox AI - Free")
st.title("Firebox AI Assistant")

# Memory Slider
memory_depth = st.sidebar.slider("Memory Depth", min_value=1, max_value=10, value=5)

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask Firebox AI...")
if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Generating response..."):
        firebox_response = ai.ask_firebox(query)
        time.sleep(3 if not is_premium else 0)  # Simulate slow response for free users

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show Firebox Premium Promotion Every 3 Minutes
if "last_premium_prompt" not in st.session_state:
    st.session_state.last_premium_prompt = time.time()

if time.time() - st.session_state.last_premium_prompt > 180:
    st.sidebar.warning("🔥 Upgrade to Firebox Premium for ultra-fast responses, premium UI, and voice support!")
    st.session_state.last_premium_prompt = time.time()
