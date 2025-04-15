#server\server.py
from flask import Flask, request, jsonify
from .auth import check_user_permissions
from .notifications import send_notification

app= Flask(__name__)

@app.route('/send_notifications', methods=['POST'])
def notify():
    user = reguest.json.get('user')
    notification_message = request.json.get('message')

    if not sheck_user_permissions(user):
        return jsonify({"error": "Unauthorized adcess"}), 403
    
    send_notification (user, notification_message)
    return jsonify({"message": "Notification sent successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 