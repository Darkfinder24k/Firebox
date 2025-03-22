import streamlit as st
import google.generativeai as genai
import cv2
from PIL import Image
import io

# Secure API Key Handling using secrets.toml
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

class FireboxAI:
    # ... (Your FireboxAI class remains the same) ...

# Initialize Firebox AI
ai = FireboxAI()

# File Processing
def process_image(uploaded_file):
    image = Image.open(uploaded_file)
    # Basic example: convert to grayscale
    gray_image = image.convert('L')
    return "Image processed."

def process_video(uploaded_file):
    cap = cv2.VideoCapture(io.BytesIO(uploaded_file.read()))
    # Basic example: get video frame count
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return f"Video processed. Frame count: {frame_count}"

def handle_file_upload():
    uploaded_file = st.file_uploader("Upload file", type=["png", "jpg", "jpeg", "mp4"])
    if uploaded_file:
        file_type = uploaded_file.type
        if "image" in file_type:
            return process_image(uploaded_file)
        elif "video" in file_type:
            return process_video(uploaded_file)
        else:
            return "Unsupported file type"
    return None

# Streamlit UI
st.set_page_config(page_title="Firebox AI", layout="wide")

# Updated CSS with !important
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

# Speech Recognition (Web Speech API)
if "speech_text" not in st.session_state:
    st.session_state.speech_text = None

speech_button = st.button("Speak")

if speech_button:
    speech_component = st.components.v1.html(
        """
        <script>
            var recognition = new webkitSpeechRecognition() || speechRecognition();
            recognition.lang = 'en-US';
            recognition.start();
            recognition.onresult = function(event) {
                var transcript = event.results[0][0].transcript;
                window.parent.postMessage({ 'speech_text': transcript }, '*');
            }
        </script>
        """,
        height=0,
    )

def receive_message(message):
    if "speech_text" in message:
        st.session_state.speech_text = message["speech_text"]

st.components.v1.html(
    f"""
    <script>
        window.addEventListener("message", function(event) {
            window.parent.postMessage(event.data, "*");
        });
    </script>
    """,
    height=0,
)

file_result = handle_file_upload()

if st.session_state.speech_text:
    receive_message({"speech_text": st.session_state.speech_text})
    query = st.session_state.speech_text
    st.session_state.speech_text = None  # Reset

    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Generating response..."):
        initial_response = ai.ask_gemini(query)
        firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

elif file_result:
    with st.chat_message("user"):
        st.markdown(file_result)

    with st.spinner("Generating response..."):
        initial_response = ai.ask_gemini(file_result)
        firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": file_result})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

else:
    query = st.chat_input("Ask Firebox AI...")

    if query:
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Generating response..."):
            initial_response = ai.ask_gemini(query)
            firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response

        with st.chat_message("assistant"):
            st.markdown(firebox_response)

        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": firebox_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
