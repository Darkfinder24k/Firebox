import streamlit as st
import google.generativeai as genai
from PIL import Image
import traceback
import sys  # Import sys for more detailed error reporting

# --- Configuration and Error Handling ---
try:
    GEMINI_API_KEY = st.secrets["google"]["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    st.error("API key not found in secrets.toml. Please ensure it is correctly configured.")
    st.stop()
except Exception as e:
    st.error(f"Error configuring API: {e}\n{traceback.format_exc()}")
    st.stop()

# --- Firebox AI Class ---
class FireboxAI:
    # ... (FireboxAI class remains the same)

# --- Image Processing ---
def process_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        gray_image = image.convert('L')
        return "Image processed successfully."
    except Exception as e:
        st.error(f"Error processing image: {e}\n{traceback.format_exc()}")
        return "Failed to process image."

# --- File Upload Handler ---
def handle_file_upload():
    try:
        uploaded_file = st.file_uploader("Upload file", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            file_type = uploaded_file.type
            if "image" in file_type:
                return process_image(uploaded_file)
            else:
                return "Unsupported file type."
        return None
    except Exception as e:
        st.error(f"File upload error: {e}\n{traceback.format_exc()}")
        return "File upload failed."

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Firebox AI", layout="wide")

st.markdown(
    """
    <style>
        #MainMenu, footer, header, .viewerBadge_container__1QSob, .viewerBadge_link__1S1BI, .viewerBadge_button__13la3, .css-1y4p8pa {
            visibility: hidden !important;
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
ai = FireboxAI() #Initialize AI here.

# --- Main Logic ---
try:
    file_result = handle_file_upload()
    query = st.chat_input("Ask Firebox AI...")

    if file_result:
        with st.chat_message("user"):
            st.markdown(file_result)
        with st.spinner("Generating response..."):
            initial_response = ai.ask_gemini(file_result)
            firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response
        with st.chat_message("assistant"):
            st.markdown(firebox_response)
        st.session_state.messages.append({"role": "user", "content": file_result})
        st.session_state.messages.append({"role": "assistant", "content": firebox_response})

    elif query:
        with st.chat_message("user"):
            st.markdown(query)
        with st.spinner("Generating response..."):
            initial_response = ai.ask_gemini(query)
            firebox_response = ai.refine_response(initial_response) if refine_response_enabled else initial_response
        with st.chat_message("assistant"):
            st.markdown(firebox_response)
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.messages.append({"role": "assistant", "content": firebox_response})

    # --- Display Messages ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

except Exception as e:
    st.error(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
    st.error(f"Python version: {sys.version}") #Print python version.
    st.error(f"Streamlit version: {st.__version__}") #print streamlit version.
    st.stop() #Stops the app.
