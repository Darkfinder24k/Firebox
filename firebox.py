import streamlit as st
import google.generativeai as genai

# Set API key
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

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
        """Refines the response to be more detailed, sympathetic, and well-structured."""
        try:
            improved_response = self.model.generate_content(
                f"Rewrite the following response in a more informative, empathetic, and structured way, without saying a word else! because i want the response for my ai:\n\n{response}",
                generation_config={"max_output_tokens": 2048}  # Prevents cut-off responses
            )
            refined_text = improved_response.text if improved_response else response
            return self.replace_your(refined_text)  # Apply replacement
        except Exception as e:
            return response  # Fallback in case of error

    def replace_your(self, text):
        """Replaces 'your' with Firebox AI's description."""
        if "your" in text.lower():  # Check if 'your' is in response
            return text.replace("your", "Firebox AI, created by Kushagra Srivastava, its")
        return text

# Initialize Firebox AI
ai = FireboxAI()

# Streamlit UI
st.set_page_config(page_title="Firebox AI", layout="wide")
st.sidebar.title("🔥 Firebox AI")
st.title("Firebox AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask Firebox AI...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    initial_response = ai.ask_gemini(query)
    firebox_response = ai.refine_response(initial_response)

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})
