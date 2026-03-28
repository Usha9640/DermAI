#!/bin/bash
echo ""
echo " DermAI — AI Skin Disease Detection"
echo "══════════════════════════════════════"
echo ""
echo "[1/3] Installing dependencies..."
pip install -r requirements.txt
echo ""
echo "[2/3] Opening browser..."
sleep 2
if [[ "$OSTYPE" == "darwin"* ]]; then
  open http://localhost:5000
else
  xdg-open http://localhost:5000
fi
echo ""
echo "[3/3] Starting server at http://localhost:5000"
echo " Press Ctrl+C to stop"
echo ""
python app.py
