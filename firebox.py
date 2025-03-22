import streamlit as st
import google.generativeai as genai

# Set API key
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

class FireboxAI:
    def __init__(self):
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash",
            generation_config={"max_output_tokens": 2048}
        )

    def ask_gemini(self, prompt):
        """Gets the initial response from Gemini and extracts only the text."""
        try:
            response = self.model.generate_content(prompt)
            if response and hasattr(response, "candidates"):
                return response.candidates[0].content
            return "Error: No response from Firebox AI."
        except Exception as e:
            return f"Error: Firebox AI issue - {str(e)}"

    def refine_response(self, response):
        """Refines the response to be more detailed, sympathetic, and well-structured."""
        try:
            prompt = (
                "Rewrite the following response in a more informative, empathetic, and structured way:\n\n"
                f"Original Response:\n{response}"
            )
            improved_response = self.model.generate_content(prompt)
            if improved_response and improved_response.candidates:
                return improved_response.candidates[0].content
            return response
        except Exception:
            return response

# Initialize Firebox AI
ai = FireboxAI()

# 🔥 Streamlit UI
st.set_page_config(page_title="Firebox AI", layout="wide")
st.sidebar.title("🔥 Firebox AI")
st.title("Firebox AI Assistant")

# 🔹 Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🔹 Input field with Browse (File Upload) option
query = st.chat_input("Ask Firebox AI...")
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "mp3", "mp4"])

if uploaded_file is not None:
    st.write(f"📂 Uploaded file: {uploaded_file.name}")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    initial_response = ai.ask_gemini(query)
    firebox_response = ai.refine_response(initial_response)

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})
