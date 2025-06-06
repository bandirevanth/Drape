import streamlit as st
import requests
from PIL import Image
import os
from dotenv import load_dotenv

# --- Load environment and backend URL ---
load_dotenv()
BACKEND_URL = "http://127.0.0.1:5000"

# --- Page Configuration ---
st.set_page_config(page_title="Drape AI", layout="wide")
st.markdown("<h1 style='color:#ff4b4b;'>👗 Drape AI - Fashion & Culture</h1>", unsafe_allow_html=True)
st.markdown("Upload an outfit piece and get culturally-inspired fashion suggestions!")

# --- Apply Light Styling ---
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Default values for preferences ---
default_values = {
    "occasion": "Casual",
    "season": "Any",
    "gender": "Woman",
    "body_type": "Average",
    "age": "20s",
    "mood": "Confident"
}

# --- Load from session or fallback to default ---
for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload your clothing image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(Image.open(uploaded_file), caption="📸 Here's your uploaded style!", use_column_width=True)
    st.markdown("---")

    st.markdown("### 🧵 Personalize Your Style Preferences")
    remember = st.checkbox("Remember my preferences for next time", value=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        occasion = st.selectbox("🎯 Occasion", ["Casual", "Formal", "Party", "Wedding", "Work", "Date"], index=["Casual", "Formal", "Party", "Wedding", "Work", "Date"].index(st.session_state.occasion))
        season = st.selectbox("🌦️ Season", ["Any", "Summer", "Winter", "Spring", "Autumn", "Monsoon"], index=["Any", "Summer", "Winter", "Spring", "Autumn", "Monsoon"].index(st.session_state.season))
    with col2:
        gender = st.selectbox("🚻 Gender", ["Woman", "Man", "Non-binary", "Prefer not to say"], index=["Woman", "Man", "Non-binary", "Prefer not to say"].index(st.session_state.gender))
        body_type = st.selectbox("🧍 Body Type", ["Average", "Petite", "Tall", "Plus-size", "Athletic", "Curvy"], index=["Average", "Petite", "Tall", "Plus-size", "Athletic", "Curvy"].index(st.session_state.body_type))
    with col3:
        age = st.selectbox("🎂 Age Group", ["Teen", "20s", "30s", "40s", "50+", "60+"], index=["Teen", "20s", "30s", "40s", "50+", "60+"].index(st.session_state.age))
        mood = st.selectbox("😌 Mood", ["Happy", "Lazy", "Motivated", "Romantic", "Confident", "Chill", "Adventurous", "Classy", "Energetic", "Bold", "Elegant", "Sophisticated", "Edgy"], index=["Happy", "Lazy", "Motivated", "Romantic", "Confident", "Chill", "Adventurous", "Classy", "Energetic", "Bold", "Elegant", "Sophisticated", "Edgy"].index(st.session_state.mood))

    if st.button("✨ Generate Style Masterpiece"):
        with st.spinner("🪡 Stitching your perfect outfit suggestion..."):
            try:
                # Save current selections to session if checkbox is ticked
                if remember:
                    st.session_state.occasion = occasion
                    st.session_state.season = season
                    st.session_state.gender = gender
                    st.session_state.body_type = body_type
                    st.session_state.age = age
                    st.session_state.mood = mood

                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={'file': ('image.jpg', uploaded_file.getvalue(), 'image/jpeg')},
                    data={
                        "occasion": occasion,
                        "season": season,
                        "gender": gender,
                        "body_type": body_type,
                        "age": age,
                        "mood": mood
                    },
                    timeout=30
                )
                result = response.json()

                if response.status_code != 200:
                    st.error(f"❌ Server error: {result.get('message', 'Unknown')}")
                elif "fashion_suggestion" in result.get("data", {}):
                    st.markdown("### ✨ Your Fashion Suggestion")
                    st.markdown(result["data"]["fashion_suggestion"])
                else:
                    st.warning("⚠️ No suggestion returned. Try a different image or filters.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
