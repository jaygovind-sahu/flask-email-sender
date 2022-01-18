import json
import os

from flask import Flask, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.environ['mailserv']
app.config['MAIL_PORT'] = int(os.environ['mailport'])
app.config['MAIL_USERNAME'] = os.environ['mailuser']
app.config['MAIL_PASSWORD'] = os.environ['mailpass']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route("/", methods=['GET'])
def index():
    return app.response_class(
        response=json.dumps({'message': 'All is well!'}),
        status=200,
        mimetype='application/json'
    )


@app.route("/message", methods=['POST'])
def post_message():
    request_data = request.get_json()
    message = Message(f"Website message from {request_data['name']}",
                      sender=os.environ['mailuser'],
                      recipients=[os.environ['mailuser']])
    message.body = f"{request_data['message']}\n\n{request_data['name']}\n{request_data['email']}"
    mail.send(message)
    return app.response_class(
        response=json.dumps({'message': 'Message sent!'}),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run()
