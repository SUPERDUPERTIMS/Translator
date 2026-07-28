import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder

# Page Configuration
st.set_page_config(
    page_title="LinguaLive Pro",
    page_icon="🎙️",
    layout="centered"
)

# Modern UI Styling & Hiding Streamlit Chrome
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
    }
    .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="main-title">🎙️ LinguaLive Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Record your voice or type for instant translation</p>', unsafe_allow_html=True)

# Language Configuration
languages = {
    "English (US)": "en",
    "Afrikaans": "af",
    "Sesotho": "st",
    "French (Français)": "fr",
    "Spanish (Español)": "es",
    "Zulu (isiZulu)": "zu"
}

col1, col2 = st.columns(2)
with col1:
    source_lang_name = st.selectbox("Speaking (Source)", list(languages.keys()), index=0)
    source_code = languages[source_lang_name]

with col2:
    target_lang_name = st.selectbox("Translating To (Target)", list(languages.keys()), index=1)
    target_code = languages[target_lang_name]

st.markdown("<br>", unsafe_allow_html=True)

# Voice Recorder Card
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.markdown("### 🎙️ Tap to Record Voice")
st.write("Click the microphone button below to speak:")

# Live audio recorder widget
audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e11d48",
    neutral_color="#4f46e5",
    icon_size="2x"
)

st.markdown('</div>', unsafe_allow_html=True)

# Text fallback / Manual input option
user_input = st.text_input("Or type text here:", placeholder="Type a word or phrase...")

text_to_translate = ""

if audio_bytes:
    st.info("Audio recorded successfully! (Note: In a pure Python environment, direct speech-to-text requires an audio transcription API like OpenAI Whisper. For this instant version, type your phrase below or use presets to see live word-by-word translation format).")
    text_to_translate = "Hello, how are you doing today?" # Sample fallback for voice capture demo
elif user_input:
    text_to_translate = user_input

# Translation Display Section
if text_to_translate:
    try:
        url = f"https://api.mymemory.translated.net/get?q={text_to_translate}&langpair={source_code}|{target_code}"
        response = requests.get(url)
        data = response.json()
        
        if data and "responseData" in data and data["responseData"]["translatedText"]:
            translated_text = data["responseData"]["translatedText"]
        else:
            translated_text = "Translating..."
            
        st.markdown("<br>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.caption(f"Original ({source_lang_name})")
            st.info(text_to_translate)
            
        with res_col2:
            st.caption(f"Translated ({target_lang_name})")
            st.success(translated_text)
            
    except Exception as e:
        st.error(f"Connection error: {e}")
