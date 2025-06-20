# DrapeAI - Your AI-Powered Fashion Assistant

DrapeAI is an intelligent fashion recommendation app that helps users match outfits based on mood, occasion, season, age, and body type - powered by OpenAI and Streamlit.

Upload your clothing item image and get AI-personalized styling tips. ✨

Completely offline-compatible, no cloud functions or sign-ups/logins...

---

## 🚀 Features

✅ Upload clothing image (JPG/PNG)  
✅ Select style preferences (Occasion, Season, Mood, Age, Body Type)  
✅ Get smart AI-powered outfit suggestions  
✅ Listen to recommendations using built-in text-to-speech  
✅ Explore fashion tips for Travel & Trends  
✅ UI with backgrounds and intuitive layout

---

## 🛠️ Built With
Streamlit, OpenAI AI, Pillow, Flask

---

Don't forget to star me on GitHub and follow me! Thanks :)

---

## 💻 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/bandirevanth/Drape.git
cd Drape

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # for Windows

#3. Add your .env file:
env OPENAI_API_KEY=your_key_here

# 3. Install requirements
pip install -r requirements.txt

# 4. Run the app
streamlit run frontend.py

