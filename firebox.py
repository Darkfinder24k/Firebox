import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io

# Secure API Key Handling using secrets.toml
GEMINI_API_KEY = "AIzaSyD9hmqBaXvZqAUxQ3mnejzM_EwPMeZQod4"
genai.configure(api_key=GEMINI_API_KEY)

class FireboxAI:
    # ... (Your FireboxAI class remains the same)

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

        .search-bar-container {
            display: flex;
            align-items: center;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px;
        }

        .search-input {
            flex-grow: 1;
            padding: 8px;
            border: none;
        }

        .plus-button {
            cursor: pointer;
            padding: 8px;
            border: none;
            background-color: transparent;
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

# Custom Search Bar with Plus Button
search_bar_html = """
<div class="search-bar-container">
    <input type="text" class="search-input" id="search-input" placeholder="Ask Firebox AI...">
    <button class="plus-button" id="plus-button">+</button>
    <input type="file" id="file-input" style="display: none;" accept="image/*">
</div>

<script>
    const plusButton = document.getElementById("plus-button");
    const fileInput = document.getElementById("file-input");
    const searchInput = document.getElementById("search-input");

    plusButton.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const base64Image = e.target.result;
                window.parent.postMessage({ type: "file_upload", data: base64Image }, "*");
            };
            reader.readAsDataURL(file);
        }
    });

    searchInput.addEventListener("change", (event)=>{
        const query = event.target.value;
        window.parent.postMessage({ type: "text_input", query: query }, "*");
    })

</script>
"""

def handle_message(message):
    if message.get('type') == 'file_upload':
        try:
            image_data = message['data'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            file_result = process_image(image)

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

        except Exception as e:
            st.error(f"Error processing uploaded image: {e}")

    elif message.get('type') == 'text_input':
        query = message['query']
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

st.components.v1.html(search_bar_html, height=50, on_message=handle_message)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
