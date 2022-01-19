import os

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = int(os.environ['MAIL_PORT'])
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route("/", methods=['GET'])
def index():
    response = app.response_class(
        response=jsonify({'message': 'All is well!'}),
        status=200,
        mimetype='application/json'
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/message", methods=['POST'])
@cross_origin()
def post_message():
    request_data = request.get_json()
    if not (request_data.get('name', '') or request_data.get('email', '') or request_data.get('message', '')):
        return app.response_class(
            response=jsonify({'error': 'Fields validation failed.'}),
            status=400,
            mimetype='application/json'
        )
    message = Message(f"Website message from {request_data['name']}",
                      sender=os.environ['MAIL_USERNAME'],
                      recipients=[os.environ['MAIL_USERNAME']])
    message.body = f"{request_data['message']}\n\n{request_data['name']}\n{request_data['email']}"
    mail.send(message)
    return app.response_class(
        response=jsonify({'message': 'Message sent!'}),
        status=200,
        mimetype='application/json'
    )
