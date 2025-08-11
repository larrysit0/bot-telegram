import os
import logging
from flask import Flask, request, jsonify
import requests

# Configuración
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://alarma-production.up.railway.app")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN no está configurado")

# Configuración de Flask
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    r = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)
    r.raise_for_status()
    return r.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    logging.info(f"📩 Update recibido: {update}")

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        from_user = message.get("from", {})

        # Caso MIREGISTRO
        if text.upper() == "MIREGISTRO":
            user_id = from_user.get("id")
            first_name = from_user.get("first_name", "Usuario")
            logging.info(f"🆔 Usuario solicitó MIREGISTRO: {user_id} - {first_name}")
            send_message(chat_id, f"Tu ID de Telegram es: <b>{user_id}</b>")

        # Caso SOS
        elif text.upper() == "SOS":
            community_param = "mi_comunidad"  # Aquí puedes mapear según el grupo
            url_with_params = f"{WEBAPP_URL}/?comunidad={community_param}&id={from_user.get('id')}&first_name={from_user.get('first_name')}"
            reply_markup = {
                "inline_keyboard": [
                    [{"text": "🚨 Abrir Botón de Emergencia", "web_app": {"url": url_with_params}}]
                ]
            }
            send_message(chat_id, "Presiona el botón para abrir la WebApp de Emergencia:", reply_markup)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
