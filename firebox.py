import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from PIL import Image
import time

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

    def ask_firebox(self, prompt, refine_times=0):
        try:
            response = self.model.generate_content(prompt)
            output = response.text if response else "Error: No response."
            
            if is_premium:
                for _ in range(refine_times):  # Refining for premium users
                    response = self.model.generate_content(output)
                    output = response.text if response else output
            
            return output
        except Exception as e:
            st.error(f"Error: Firebox AI encountered an issue - {str(e)}")
            return "An error occurred. Please try again later."

# Initialize Firebox AI
ai = FireboxAI(is_premium)

# Streamlit UI
st.set_page_config(page_title="Firebox AI", layout="wide")
st.sidebar.title("🔥 Firebox AI - Very Pro Premium" if is_premium else "🔥 Firebox AI - Free")
st.title("Firebox AI Assistant")

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

# Memory Slider
memory_depth = st.sidebar.slider("Memory Depth", min_value=1, max_value=10, value=5)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🎙️ Use Voice Input"):
    speech_text = recognize_speech()
    if speech_text:
        with st.chat_message("user"):
            st.markdown(speech_text)

        with st.spinner("Generating response..."):
            firebox_response = ai.ask_firebox(speech_text, refine_times=10 if is_premium else 0)
            time.sleep(3)  # Simulating slower response generation for free users

        with st.chat_message("assistant"):
            st.markdown(firebox_response)

        st.session_state.messages.append({"role": "user", "content": speech_text})
        st.session_state.messages.append({"role": "assistant", "content": firebox_response})

query = st.chat_input("Ask Firebox AI...")
if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Generating response..."):
        firebox_response = ai.ask_firebox(query, refine_times=10 if is_premium else 0)
        time.sleep(3)  # Simulating slower response generation for free users

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
