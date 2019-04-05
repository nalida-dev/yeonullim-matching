from flask import Flask, jsonify, request
from threading import Thread
import requests
import sys

from matching import Problem, SolverPlain

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
                { 'text': quoted }
            ]
        }
    else:
        return {
            'response_type': 'in_channel',
            'text': text,
        }

def solve_plain(problem, send):
    solver = SolverPlain(problem)
    send(text_response('계산 결과가 도착했습니다. 아무렇게나 나눠보고 제일 좋은 걸 찾은 거니까 혹시 맘에 안 들면 다시 계산을 시켜주세요!', solver.solve()))

def validity_check(command, query, send):
    problem = Problem(query)
    if problem.problem:
        send(text_response('네. 아래와 같은 입력을 받았습니다. 잠시만 기다려주세요!', problem.description))
        thread = Thread(target=solve_plain, args=(problem, send), daemon=True)
        thread.start()
    else:
        send(text_response('입력이 잘못된 것 같아요. 다시 확인해주세요!', problem.description))

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
