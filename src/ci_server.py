import logging
from flask import Flask, request, jsonify
from webhook_handler import process_webhook
from notifier import send_notification

# Initialize Flask app for webhook handling
app = Flask(__name__)

# Handle incoming webhook requests
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handles incoming webhook events from GitHub and triggers necessary actions."""
    payload = request.json
    response = process_webhook(payload)
    return response

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting CI server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
