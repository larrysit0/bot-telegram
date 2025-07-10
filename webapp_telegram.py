import os
import requests
import time

# 🔐 Token del bot desde variable de entorno (Railway)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Lista de comunidades con su chat_id y nombre
comunidades = {
    "-1002585455176": "brisas",
    "-987654321": "miraflores",
    "-111222333": "condores"
}

# 🌐 URL base de la WebApp
BASE_URL = "https://alarma-production.up.railway.app"

def enviar_boton(chat_id, nombre):
    url_webapp = f"{BASE_URL}/?comunidad={nombre}"
    payload = {
        "chat_id": chat_id,
        "text": f"🚨 Abre la alarma de la comunidad: {nombre.upper()}",
        "reply_markup": {
            "keyboard": [[{
                "text": "🚨 ABRIR ALARMA VECINAL",
                "web_app": {
                    "url": url_webapp
                }
            }]],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    }
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json=payload
    )
    if response.ok:
        print(f"✅ Botón enviado para {nombre}")
    else:
        print(f"❌ Error al enviar botón para {nombre}: {response.text}")

def obtener_actualizaciones(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()

def main():
    last_update_id = None
    while True:
        data = obtener_actualizaciones(last_update_id)
        for update in data.get("result", []):
            last_update_id = update["update_id"] + 1
            message = update.get("message") or update.get("edited_message")
            if not message:
                continue

            text = message.get("text", "").lower()
            chat = message.get("chat", {})
            chat_id = str(chat.get("id"))

            # Verifica si el mensaje fue "sos" y el chat está en la lista
            if text == "sos" and chat_id in comunidades:
                nombre = comunidades[chat_id]
                enviar_boton(chat_id, nombre)

        time.sleep(2)

if __name__ == "__main__":
    main()
