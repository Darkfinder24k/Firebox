import streamlit as st
import ollama
import google.generativeai as genai
import speech_recognition as sr
import bcrypt
import smtplib
from email.mime.text import MIMEText
import random
import pandas as pd
import os
from PIL import Image
import cv2
import numpy as np
from streamlit_option_menu import option_menu

# Configure Gemini API
genai.configure(api_key="AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4")

# Set up user database file
USER_DB = "users.xlsx"
if not os.path.exists(USER_DB):
    df = pd.DataFrame(columns=["Username", "Email", "Password"])
    df.to_excel(USER_DB, index=False)


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode(), hashed_password.encode())


def send_verification_email(email, code):
    try:
        sender_email = "your_email@example.com"
        sender_password = "your_email_password"
        message = MIMEText(f"Your verification code is: {code}")
        message["Subject"] = "Firebox AI Email Verification"
        message["From"] = sender_email
        message["To"] = email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False


def generate_verification_code():
    return str(random.randint(100000, 999999))


def get_ai_response(prompt):
    special_questions = ["who are you", "who made you", "which company", "how were you made", "api"]
    if any(q in prompt.lower() for q in special_questions):
        return "Kushagra made me, and I am from a company named Firebox."

    model = 'llama3.2'
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response.get('message', {}).get('content', '').strip()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Could not recognize speech."


def process_image(image_file):
    img_array = np.array(Image.open(image_file))
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    return f"Image uploaded successfully."


def process_video(video_file):
    return "Video uploaded successfully."


st.set_page_config(page_title="Firebox AI", page_icon=":fire:", layout="wide")
st.markdown("""<style>body {background-color: black; color: white;} footer {visibility: hidden;}</style>""",
            unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.logged_in:
    menu = option_menu(None, ["Login", "Signup"], icons=['box-arrow-in-right', 'person-add'], menu_icon="cast",
                       default_index=0, orientation="horizontal")
    df = pd.read_excel(USER_DB)

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_row = df[df["Username"] == username]
            if not user_row.empty and verify_password(password, user_row.iloc[0]["Password"]):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")
    elif menu == "Signup":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if username in df["Username"].values:
                st.error("Username already exists")
            else:
                verification_code = generate_verification_code()
                if send_verification_email(email, verification_code):
                    entered_code = st.text_input("Enter the verification code sent to your email")
                    if st.button("Verify"):
                        if entered_code == verification_code:
                            new_user = pd.DataFrame([[username, email, hash_password(password)]],
                                                    columns=["Username", "Email", "Password"])
                            df = pd.concat([df, new_user], ignore_index=True)
                            df.to_excel(USER_DB, index=False)
                            st.success("Account created successfully. Please login.")
                        else:
                            st.error("Incorrect verification code")
else:
    with st.sidebar:
        st.title("Firebox AI")
        st.write(f"Welcome, {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.experimental_rerun()

    st.title("Chat with Firebox AI")
    user_input = st.text_input("You: ")
    if st.button("Send"):
        response = get_ai_response(user_input)
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Firebox", response))

    for role, text in st.session_state.messages:
        st.write(f"**{role}:** {text}")

    if st.button("Use Voice Input"):
        speech_text = recognize_speech()
        st.text(f"Recognized: {speech_text}")
        response = get_ai_response(speech_text)
        st.session_state.messages.append(("You", speech_text))
        st.session_state.messages.append(("Firebox", response))

    uploaded_file = st.file_uploader("Upload an Image or Video", type=["png", "jpg", "jpeg", "mp4"])
    if uploaded_file:
        if uploaded_file.type.startswith("image"):
            result = process_image(uploaded_file)
        else:
            result = process_video(uploaded_file)
        st.text(result)
