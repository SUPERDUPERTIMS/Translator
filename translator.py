import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="LinguaLive - Speech Translator",
    page_icon="🌍",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4f46e5, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-title">🌍 LinguaLive Translator</p>', unsafe_allow_html=True)
st.write("Translate phrases instantly between languages like English, Afrikaans, Sesotho, French, and more.")

# Language Selection Bar
col1, col2 = st.columns(2)

languages = {
    "English (US)": "en",
    "Afrikaans": "af",
    "Sesotho": "st",
    "French (Français)": "fr",
    "Spanish (Español)": "es",
    "Zulu (isiZulu)": "zu"
}

with col1:
    source_lang_name = st.selectbox("Speaking (Source)", list(languages.keys()), index=0)
    source_code = languages[source_lang_name]

with col2:
    # Default target to Afrikaans as a handy preset
    target_lang_name = st.selectbox("Translating To (Target)", list(languages.keys()), index=1)
    target_code = languages[target_lang_name]

st.divider()

# Text Input Area (Since web audio streaming in pure Python requires custom WebRTC components, 
# text input paired with instant API translation gives a rock-solid, lightning-fast experience on Streamlit Cloud)
st.markdown("### 💬 Live Translation Input")
user_input = st.text_area("Type or paste what you want to translate:", placeholder="Type something here...", height=100)

if user_input:
    try:
        # Using MyMemory translation API
        url = f"https://api.mymemory.translated.net/get?q={user_input}&langpair={source_code}|{target_code}"
        response = requests.get(url)
        data = response.json()
        
        if data and "responseData" in data and data["responseData"]["translatedText"]:
            translated_text = data["responseData"]["translatedText"]
        else:
            translated_text = "Translation service temporarily busy."
            
        # Display Results side by side
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown(f"**Original ({source_lang_name})**")
            st.info(user_input)
            
        with res_col2:
            st.markdown(f"**Translated ({target_lang_name})**")
            st.success(translated_text)
            
    except Exception as e:
        st.error(f"Could not reach translation service: {e}")
else:
    st.caption("Start typing above to see the live translation update instantly.")
