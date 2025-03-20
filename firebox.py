import streamlit as st
import google.generativeai as genai

# Set API key (directly, without os)
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"  # Replace with your actual API key

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("Missing Gemini API Key. Set it as an environment variable.")

class FireboxAI:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def ask_gemini(self, prompt):
        """Gets the initial response from Gemini."""
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else "Error: No response from Firebox AI."
        except Exception as e:
            return f"Error: Firebox AI issue - {str(e)}"

    def refine_response(self, response):
        """Refines the response to be more informative, sympathetic, and well-structured."""
        try:
            improved_response = self.model.generate_content(
                f"Make this response more detailed, sympathetic, and well-structured General, Empathetic & Proactive, General and Empathetic, without saying anything else, other than the response: {response}"
            )
            return improved_response.text if improved_response else response
        except Exception as e:
            return response  # If refining fails, return the original response

# Initialize Firebox AI
ai = FireboxAI()

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

    # Step 1: Get the initial response
    initial_response = ai.ask_gemini(query)

    # Step 2: Refine the response
    firebox_response = ai.refine_response(initial_response)

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    # Save conversation
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})
