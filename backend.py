import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

app = Flask(__name__)
CORS(app)

class WhatsAppAgent:
    def __init__(self, instance_id, token):
        self.instance_id = instance_id
        self.token = token

    def send_message(self, phone, message):
        url = f"https://api.ultramsg.com/{self.instance_id}/messages/chat"
        payload = {
            "token": self.token,
            "to": phone,
            "body": message,
        }
        response = requests.post(url, data=payload)
        try:
            data = response.json()
            if data.get("sent") == "true" or data.get("message") == "ok":
                return True
            else:
                return False
        except Exception:
            return False

agent = WhatsAppAgent(ULTRAMSG_INSTANCE_ID, ULTRAMSG_TOKEN)

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    phone = data.get("phone")
    message = data.get("message")
    if not phone or not message:
        return jsonify({"error": "Missing phone or message"}), 400
    success = agent.send_message(phone, message)
    if success:
        return jsonify({"sent": "true"})
    else:
        return jsonify({"sent": "false"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True) 