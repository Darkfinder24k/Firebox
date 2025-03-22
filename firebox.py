import streamlit as st
import google.generativeai as genai
from PIL import Image

# Secure API Key Handling using secrets.toml
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

class FireboxAI:
    def __init__(self, model_name="gemini-2.0-flash", max_tokens=2048):
        self.model = genai.GenerativeModel(
            model_name, generation_config={"max_output_tokens": max_tokens}
        )

    def ask_gemini(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text if response else "Error: No response from Firebox AI."
        except Exception as e:
            st.error(f"Error: Firebox AI encountered an issue - {str(e)}")
            return "An error occurred. Please try again later."

    def refine_response(self, response, refine_prompt=None):
        if not refine_prompt:
            refine_prompt = (
                "Rewrite the following response in a more informative, empathetic, and structured way, More General and Welcoming, Slightly More Formal. "
                "If the input contains 'your' or 'you're', replace them with: "
                "'Firebox AI, created by Kushagra Srivastava, is a cutting-edge AI assistant designed to provide "
                "smart, insightful, and highly adaptive responses.'\n\n"
                f"Original Response:\n{response}"
            )
        try:
            improved_response = self.model.generate_content(refine_prompt)
            if improved_response and improved_response.text:
                return self.replace_your(improved_response.text)
            else:
                return response
        except Exception as e:
            st.error(f"Error during response refinement: {str(e)}")
            return response

    def replace_your(self, text):
        description = (
            "Firebox AI, created by Kushagra Srivastava, is a cutting-edge AI assistant designed to provide "
            "smart, insightful, and highly adaptive responses."
        )
        return text.replace("your", description).replace("Your", description).replace("you're", description).replace("You're", description)

# Initialize Firebox AI
ai = FireboxAI()

# Image Processing
def process_image(uploaded_file):
    image = Image.open(uploaded_file)
    gray_image = image.convert('L')
    return "Image processed."

# Streamlit UI
st.set_page_config(page_title="Firebox AI", layout="wide")

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden !important;}
        header {visibility: hidden;}
        .viewerBadge_container__1QSob, .viewerBadge_link__1S1BI, .viewerBadge_button__13la3 {
            display: none !important; 
        }
        .css-1y4p8pa {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("🔥 Firebox AI")
st.title("Firebox AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

refine_response_enabled = st.sidebar.checkbox("Refine Response", value=True)

# File Upload Button
uploaded_file = st.file_uploader("Upload file", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_type = uploaded_file.type
    if "image" in file_type:
        file_result = process_image(uploaded_file)
    else:
        file_result = "Unsupported file type"

    with st.chat_message("user"):
        st.markdown(file_result)

    with st.spinner("Generating response..."):
        try:
            initial_response = ai.ask_gemini(file_result)
            firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response
        except Exception as e:
            st.error(f"Error generating response: {e}")
            firebox_response = "An error occurred generating the response."

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": file_result})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

# Text Input
query = st.chat_input("Ask Firebox AI...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Generating response..."):
        try:
            initial_response = ai.ask_gemini(query)
            firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response
        except Exception as e:
            st.error(f"Error generating response: {e}")
            firebox_response = "An error occurred generating the response."

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
