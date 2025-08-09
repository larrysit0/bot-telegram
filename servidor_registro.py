import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Esta ruta principal sirve el HTML del botón de registro
@app.route('/')
def index():
    return render_template('index.html')

# Esta ruta estática sirve el JavaScript para la WebApp
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

# Este endpoint recibe el ID de Telegram enviado desde la WebApp
@app.route('/api/register', methods=['POST'])
def register_id():
    try:
        data = request.json
        telegram_id = data.get('telegram_id')
        user_info = data.get('user_info', {})
        
        if telegram_id:
            print(f"ID de Telegram recibido: {telegram_id}")
            print(f"Información de usuario: {user_info}")
            # Aquí podrías agregar lógica para guardar el ID en un archivo o base de datos
            return jsonify({"status": "ID recibido y registrado."}), 200
        else:
            return jsonify({"error": "ID no proporcionado"}), 400
    except Exception as e:
        print(f"Error en /api/register: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
