from flask import Flask, jsonify, request
from threading import Thread
import requests
import sys

from matching import Problem

app = Flask(__name__)

def send_to(response_url):
    def send(response):
        return requests.post(response_url, json=response)
    return send

def text_response(text, quoted=None):
    if quoted:
        return {
            'response_type': 'in_channel',
            'text': text,
            'attachments': [
                { 'text': text }
            ]
        }
    else:
        return {
            'response_type': 'in_channel',
            'text': text,
        }

def validity_check(command, query, send):
    problem = Problem(query)
    send(text_response(problem.description))

def start_query(command, query, send):
    thread = Thread(target=validity_check, args=(command, query, send), daemon=True)
    thread.start()
    
@app.route("/", methods=["GET", "POST"])
def main():
    print(request.form)
    command = request.form['command']
    text = request.form['text']
    response_url = request.form['response_url']
    start_query(command, text, send_to(response_url))
    return jsonify(text_response(''))

app.run(host=sys.argv[1], port=sys.argv[2])
