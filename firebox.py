import streamlit as st
import google.generativeai as genai

# Set API key
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

class FireboxAI:
    def __init__(self):
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash",
            generation_config={"max_output_tokens": 2048}  # Set config at initialization
        )

    def ask_gemini(self, prompt):
        """Gets the initial response from Gemini and extracts only the text."""
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else "Error: No response from Firebox AI."
        except Exception as e:
            return f"Error: Firebox AI issue - {str(e)}"

    def refine_response(self, response):
        """Refines the response to be more detailed, sympathetic, and well-structured."""
        try:
            prompt = (
                "Rewrite the following response in a more informative, empathetic, and structured way, More General and Welcoming, Slightly More Formal. "
                "If the input contains 'your' or 'you're', replace them with: "
                "'Firebox AI, created by Kushagra Srivastava, is a cutting-edge AI assistant designed to provide "
                "smart, insightful, and highly adaptive responses.'\n\n"
                f"Original Response:\n{response}"
            )
            improved_response = self.model.generate_content(prompt)
            return self.replace_your(improved_response.text) if improved_response else response
        except Exception as e:
            return response  # Fallback if an error occurs

    def replace_your(self, text):
        """Replaces variations of 'your' with Firebox AI's description."""
        description = (
            "Firebox AI, created by Kushagra Srivastava, is a cutting-edge AI assistant designed to provide "
            "smart, insightful, and highly adaptive responses."
        )
        text = text.replace("your", description).replace("Your", description)
        text = text.replace("you're", description).replace("You're", description)
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
