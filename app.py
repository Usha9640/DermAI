"""
DermAI Flask Backend — app.py
Voice-enabled Skin Disease Detection + Chatbot API
Updated: Groq API (Free, Works in India)
"""

import os
import uuid
import traceback
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv

# ── Load environment variables from .env file ─────────────────────────────────
load_dotenv()

# ── Keras import shim ────────────────────────────────────────────────────────
import tensorflow as tf
import tf_keras
from tf_keras.models import load_model
from tf_keras.preprocessing import image as keras_image

# ── Groq API (Free) ───────────────────────────────────────────────────────────
try:
    from groq import Groq
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GROQ_CLIENT = Groq(api_key=GROQ_API_KEY)
    GROQ_AVAILABLE = True if GROQ_API_KEY else False
except ImportError:
    GROQ_AVAILABLE = False

# ── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

# ── CNN Model ────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "skindisease.h5")
model = None

INDEX = ["Acne", "Melanoma", "Peeling skin", "Ring worm", "Vitiligo"]

DISEASE_INFO = {
    "Acne": {
        "emoji":       "🔴",
        "severity":    "Mild-Moderate",
        "description": "Inflammatory skin condition affecting sebaceous follicles, causing pimples, blackheads and whiteheads.",
        "tip":         "Use a gentle salicylic acid cleanser and avoid touching your face.",
        "prevalence":  "Affects ~85% of people aged 12-24 at some point.",
    },
    "Melanoma": {
        "emoji":       "🟤",
        "severity":    "Severe",
        "description": "A serious form of skin cancer that develops in the melanocytes (pigment-producing cells).",
        "tip":         "Seek immediate medical evaluation — early detection is critical.",
        "prevalence":  "~100,000 new cases diagnosed in the US annually.",
    },
    "Peeling skin": {
        "emoji":       "🟡",
        "severity":    "Mild",
        "description": "Superficial skin shedding caused by sunburn, contact dermatitis, or excessive dryness.",
        "tip":         "Apply fragrance-free moisturizer and avoid further UV exposure.",
        "prevalence":  "Extremely common; affects most people at some point.",
    },
    "Ring worm": {
        "emoji":       "🟠",
        "severity":    "Moderate",
        "description": "Contagious fungal infection (tinea) producing ring-shaped, scaly, itchy patches.",
        "tip":         "Apply topical antifungal cream (e.g., clotrimazole) twice daily for 2-4 weeks.",
        "prevalence":  "One of the most common fungal infections worldwide.",
    },
    "Vitiligo": {
        "emoji":       "⚪",
        "severity":    "Chronic",
        "description": "Autoimmune condition causing loss of skin pigmentation in irregular patches.",
        "tip":         "Use high-SPF sunscreen on depigmented areas; consult a dermatologist for treatment options.",
        "prevalence":  "Affects ~1-2% of the global population.",
    },
}


def load_cnn_model():
    global model
    if not os.path.exists(MODEL_PATH):
        print(f"Warning: Model file not found: {MODEL_PATH}")
        return
    try:
        model = load_model(MODEL_PATH, compile=False)
        print(f"CNN model loaded — output shape: {model.output_shape}")
    except Exception as e:
        print(f"Failed to load model: {e}")
        traceback.print_exc()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict_page():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot_page():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({
        "ok":     True,
        "model":  model is not None,
        "labels": INDEX,
    })


# ── CNN Prediction API ───────────────────────────────────────────────────────

@app.route("/api/predict", methods=["POST"])
def api_predict():
    if model is None:
        return jsonify({"success": False, "error": "Model not loaded. Check server logs."}), 503

    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image field in request."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type. Use JPG, PNG or WEBP."}), 400

    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(filepath)
        img   = keras_image.load_img(filepath, target_size=(64, 64))
        x     = keras_image.img_to_array(img)
        x     = np.expand_dims(x, axis=0)
        preds = model.predict(x, verbose=0)
        probs = preds[0].tolist()
        top_idx   = int(np.argmax(probs))
        top_label = INDEX[top_idx]
        top_conf  = float(probs[top_idx]) * 100
        info      = DISEASE_INFO.get(top_label, {})
        scores    = {INDEX[i]: round(probs[i] * 100, 2) for i in range(len(INDEX))}

        return jsonify({
            "success":     True,
            "disease":     top_label,
            "confidence":  round(top_conf, 2),
            "scores":      scores,
            "emoji":       info.get("emoji",       "🔬"),
            "severity":    info.get("severity",    "Unknown"),
            "description": info.get("description", ""),
            "tip":         info.get("tip",         ""),
            "prevalence":  info.get("prevalence",  ""),
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


# ── Chatbot API (Groq) ────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are DermAI, an expert AI dermatologist and skincare specialist.
Answer questions about skin diseases (Acne, Melanoma, Ringworm, Vitiligo, Peeling skin,
Eczema, Psoriasis, Rosacea), sunscreen, moisturizers, and skincare ingredients.

For MELANOMA always urgently recommend consulting a dermatologist immediately.

Give product recommendations by name. Use bullet lists for clarity.
Keep answers concise and readable since they may be read aloud as voice output.

End responses with: "Disclaimer: This is educational information. Please consult a
licensed dermatologist for a proper diagnosis."
"""


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if not GROQ_AVAILABLE:
        return jsonify({
            "success": False,
            "reply": "Chatbot not configured. Please add GROQ_API_KEY to your .env file."
        })

    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"success": False, "error": "No messages provided."}), 400

    try:
        last_message = messages[-1]["content"]

        chat_response = GROQ_CLIENT.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": last_message}
            ],
            max_tokens=900,
            temperature=0.7,
        )
        reply = chat_response.choices[0].message.content
        return jsonify({"success": True, "reply": reply})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# ── Static assets ─────────────────────────────────────────────────────────────
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    load_cnn_model()
    print("\n🩺  DermAI server starting on http://localhost:5000")
    print("   Routes: /  /predict  /chatbot  /about")
    print("   API:    POST /api/predict  POST /api/chat  GET /health")
    if GROQ_AVAILABLE:
        print("   Chatbot: ✅ Groq AI ready (llama-3.3-70b-versatile)")
    else:
        print("   Chatbot: ⚠️  Add GROQ_API_KEY to your .env file")
    print()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=False)