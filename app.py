from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import openai
from werkzeug.utils import secure_filename
import traceback
from dotenv import load_dotenv
from PIL import Image

# --- Load environment ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env file")

# --- Initialize OpenAI ---
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# --- Flask Setup ---
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- Health Check ---
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

# --- Upload and Suggest ---
@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            return jsonify({"error": "Invalid file type. Only JPG, JPEG, PNG allowed."}), 400
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)

        img = Image.open(temp_path)
        img.thumbnail((800, 800))  # Resize max 800x800
        img.save(temp_path) 

        with open(temp_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode('utf-8')

        os.remove(temp_path)

        filters = {
            "occasion": request.form.get("occasion", "Casual"),
            "season": request.form.get("season", "Any"),
            "gender": request.form.get("gender", "Woman"),
            "body_type": request.form.get("body_type", "Average"),
            "age": request.form.get("age", "20s"),
            "mood": request.form.get("mood", "Confident")
        }

        prompt = f"""
You are a fashion stylist.
Generate a culturally-aware, body-type-optimized outfit suggestion using this base image and these traits:

- Occasion: {filters['occasion']}
- Season: {filters['season']}
- Gender: {filters['gender']}
- Body Type: {filters['body_type']}
- Age: {filters['age']}
- Mood: {filters['mood']}

Return in Markdown with:
## Signature Look: [Theme Name]
"🌟 Vibe: [Mood/Style]"
"👗 Garment: [Key item + detail]"
"🧥 Layer: [Adaptation layer + weather]"
"💎 Accents: [3 accessories with cultural touch]"
"📏 Fit Tip: [Fit advice based on body type]"
"⚡ Final Flair: [1-line quote to boost confidence]"
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]}
            ],
            max_tokens=1000
        )

        return jsonify({
            "status": "success",
            "data": {
            "fashion_suggestion": response.choices[0].message.content
            }
        })


    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500

# --- Run Locally ---
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)