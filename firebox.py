import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from PIL import Image

# ✅ Set Page Configuration FIRST
st.set_page_config(page_title="Firebox AI", layout="wide")

# ✅ Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Secure API Key Handling
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"  # ❗Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

# ✅ User Subscription Database (Demo - Replace with Firebase/Database)
premium_users = {"kushagra@gmail.com", "premium_user@example.com"}  # Add premium users

# ✅ User Authentication
user_email = st.sidebar.text_input("Enter your Email:")
is_premium = user_email in premium_users

# ✅ AI Model Selection (Different for Free vs Premium)
class FireboxAI:
    def __init__(self, is_premium, max_tokens=2048):
        model_name = "gemini-pro" if is_premium else "gemini-2.0-flash"
        self.model = genai.GenerativeModel(
            model_name, generation_config={"max_output_tokens": max_tokens}
        )

    def refine_response(self, initial_response):
        """Refines the AI response 10 times before returning."""
        refined_text = initial_response
        for _ in range(10):
            refined_text = self.model.generate_content(
                f"Improve this response without changing its meaning: {refined_text}"
            ).text
        return refined_text

    def ask_firebox(self, prompt, memory_depth):
        """Generates Firebox AI response, refines it 10 times, and removes Google mentions."""
        try:
            memory = "\n".join([msg["content"] for msg in st.session_state.messages[-memory_depth:]])
            full_prompt = f"Previous conversation:\n{memory}\n\nUser: {prompt}\n\nFirebox AI:"
            raw_response = self.model.generate_content(full_prompt).text
            
            # 🔥 Refine response 10 times
            refined_response = self.refine_response(raw_response)
            
            # ❌ Remove mentions of Google
            clean_response = refined_response.replace("Google", "Firebox AI")
            return clean_response
        except Exception as e:
            st.error(f"Error: Firebox AI encountered an issue - {str(e)}")
            return "An error occurred. Please try again later."

# ✅ Initialize Firebox AI
ai = FireboxAI(is_premium)

# ✅ Memory Slider
memory_depth = st.sidebar.slider("Memory Depth", min_value=1, max_value=10, value=5)

# ✅ Speech Recognition
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

# ✅ Streamlit UI
st.sidebar.title("🔥 Firebox AI - Premium" if is_premium else "🔥 Firebox AI - Free")
st.title("Firebox AI Assistant")

# ✅ Voice Input Handling
if st.sidebar.button("🎙️ Use Voice Input"):
    speech_text = recognize_speech()
    if speech_text:
        with st.chat_message("user"):
            st.markdown(speech_text)

        with st.spinner("Generating response..."):
            firebox_response = ai.ask_firebox(speech_text, memory_depth)

        with st.chat_message("assistant"):
            st.markdown(firebox_response)

        st.session_state.messages.append({"role": "user", "content": speech_text})
        st.session_state.messages.append({"role": "assistant", "content": firebox_response})

# ✅ Text Input Handling
query = st.chat_input("Ask Firebox AI...")
if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Generating response..."):
        firebox_response = ai.ask_firebox(query, memory_depth)

    with st.chat_message("assistant"):
        st.markdown(firebox_response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": firebox_response})

# ✅ Display Chat History (Without Duplicates)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
