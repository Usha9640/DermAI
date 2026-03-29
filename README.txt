
 ██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ██╗
 ██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔══██╗██║
 ██║  ██║█████╗  ██████╔╝██╔████╔██║███████║██║
 ██║  ██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║
 ██████╔╝███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

 AI-Powered Skin Disease Detection System
 Built with CNN + Flask + Claude AI + Voice Chatbot
═══════════════════════════════════════════════════

📁 PROJECT STRUCTURE
═══════════════════════════════════════════════════
DermAI/
  ├── app.py              ← Flask backend server
  ├── skindisease.h5      ← CNN model (ADD THIS FILE)
  ├── requirements.txt    ← Python dependencies
  ├── README.txt          ← This file
  ├── uploads/            ← Temp image uploads (auto-created)
  └── templates/
       └── index.html     ← Full SPA frontend (all 4 pages)

═══════════════════════════════════════════════════
🚀 HOW TO RUN
═══════════════════════════════════════════════════

STEP 1 — Add your CNN model
  Copy skindisease.h5 into this DermAI/ folder

STEP 2 — Open terminal in this folder
  In VS Code: press Ctrl + ` (backtick)

STEP 3 — Install dependencies
  pip install -r requirements.txt

STEP 4 — Run the server
  python app.py

STEP 5 — Open browser
  http://localhost:5000

═══════════════════════════════════════════════════
🌐 PAGES
═══════════════════════════════════════════════════
  http://localhost:5000/          → Home page
  http://localhost:5000/predict   → Diagnose page
  http://localhost:5000/chatbot   → Voice chatbot
  http://localhost:5000/about     → About page

═══════════════════════════════════════════════════
🔌 API ENDPOINTS
═══════════════════════════════════════════════════
  GET  /health          → Check server + model status
  POST /api/predict     → CNN skin disease prediction
  POST /api/chat        → AI dermatologist chatbot

═══════════════════════════════════════════════════
🎙️ MICROPHONE (Voice Chat)
═══════════════════════════════════════════════════
  - Open http://localhost:5000 in Chrome or Edge
  - Go to AI Chat page
  - Click the mic button
  - Browser asks "Allow microphone?" → click Allow
  - Speak your skin question
  - AI answers and reads it aloud!

═══════════════════════════════════════════════════
🧠 CNN MODEL DETAILS
═══════════════════════════════════════════════════
  File:         skindisease.h5
  Input:        64 x 64 x 3 (RGB image)
  Architecture: Conv2D → MaxPool → Flatten → Dense → Softmax
  Classes:      Acne, Melanoma, Peeling skin, Ring worm, Vitiligo
  Accuracy:     ~70%

═══════════════════════════════════════════════════
⚙️ TECH STACK
═══════════════════════════════════════════════════
  Backend:   Python, Flask, TensorFlow, Keras, NumPy
  Frontend:  HTML, CSS, JavaScript (Single Page App)
  AI:        Claude API (Vision + Chatbot)
  Voice:     Web Speech API (STT + TTS)

═══════════════════════════════════════════════════
═══════════════════════════════════════════════════
  Made with ❤️  using CNN + Flask + Claude AI
═══════════════════════════════════════════════════
