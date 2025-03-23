import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from PIL import Image

# Secure API Key Handling
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

# User Subscription Database (Demo - Replace with Firebase/Database)
premium_users = {"kushagra@gmail.com", "premium_user@example.com"}  # Add premium users here

# User Authentication
user_email = st.sidebar.text_input("Enter your Email:")
is_premium = user_email in premium_users

# AI Model Selection (Different for Free vs Premium)
class FireboxAI:
    def __init__(self, is_premium, max_tokens=2048):
        model_name = "gemini-pro" if is_premium else "gemini-2.0-flash"
        self.model = genai.GenerativeModel(
            model_name, generation_config={"max_output_tokens": max_tokens}
        )

    def ask_gemini(self, prompt, memory_depth):
        try:
            memory = "\n".join([msg["content"] for msg in st.session_state.messages[-memory_depth:]])
            full_prompt = f"Previous conversation:\n{memory}\n\nUser: {prompt}\n\nFirebox AI:"
            response = self.model.generate_content(full_prompt)
            return response.text if response else "Error: No response from Firebox AI."
        except Exception as e:
            st.error(f"Error: Firebox AI encountered an issue - {str(e)}")
            return "An error occurred. Please try again later."

# Initialize Firebox AI
ai = FireboxAI(is_premium)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Memory Slider
memory_depth = st.sidebar.slider("Memory Depth", min_value=1, max_value=10, value=5)

# Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak now")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.write(f"🗣️ You said: {text}")
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            st.error("Error with speech recognition service.")
            return None

# Streamlit UI
st.set_page_config(page_title="Firebox AI", layout="wide")
st.sidebar.title("🔥 Firebox AI - Premium" if is_premium else "🔥 Firebox AI - Free")
st.title("Firebox AI Assistant")

if st.sidebar.button("🎙️ Use Voice Input"):
    speech_text = recognize_speech()
    if speech_text:
        with st.chat_message("user"):
            st.markdown(speech_text)

        with st.spinner("Generating response..."):
            firebox_response = ai.ask_gemini(speech_text, memory_depth)

        with st.chat_message("assistant"):
            st.markdown(firebox_response)

        st.session_state.messages.append({"role": "user", "content": speech_text})
        st.session_state.messages.append({"role": "assistant", "content": firebox_response})

query = st.chat_input("Ask Firebox AI...")
if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Generating response..."):
        firebox_response = ai.ask_gemini(query, memory_depth)

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
