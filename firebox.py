import streamlit as st
import requests
import google.generativeai as genai

# Set API key (directly, without os)
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"  # Replace with your actual API key

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("Missing Gemini API Key. Set it as an environment variable.")

class AIModels:
    def __init__(self, ollama_model="llama3"):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = ollama_model

    def ask_ollama(self, prompt):
        payload = {"model": self.ollama_model, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "Error: No response from Ollama API.")
        except requests.exceptions.RequestException as e:
            return f"Error: Ollama API issue - {str(e)}"

    def ask_gemini(self, prompt):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            return response.text if response else "Error: No response from Gemini API."
        except Exception as e:
            return f"Error: Gemini API issue - {str(e)}"

    def combine_responses(self, gemini_output, ollama_output):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                f"Just merge these: '{gemini_output}' and '{ollama_output}', but DO NOT say anything about Google, Meta, Gemini, or Ollama. Instead, say Firebox AI created by Kushagra Srivastava."
            )
            return response.text if response else "Error: No response from Gemini API."
        except Exception as e:
            return f"Error: Gemini API issue - {str(e)}"


# Initialize AI model
ai = AIModels()

# Streamlit UI Layout
st.set_page_config(page_title="Firebox AI", layout="wide")

# Sidebar with navigation
st.sidebar.title("🔥 Firebox AI")
st.sidebar.markdown("Navigate through the sections:")
st.sidebar.button("Home")
st.sidebar.button("Settings")
st.sidebar.button("About Firebox")

# Title
st.title("Firebox AI Assistant")

# Chat history (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bottom Search Bar (Chat Input)
query = st.chat_input("Ask Firebox AI...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    ollama_output = ai.ask_ollama(query)
    gemini_output = ai.ask_gemini(query)
    firebox_response = ai.combine_responses(gemini_output, ollama_output)

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    # Save conversation
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})
