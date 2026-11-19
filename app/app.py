import os
import sys
from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etape6_deploiement.agent import run_agent

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'response': {'type': 'text', 'content': 'Veuillez poser une question.'}})

    agent_response = run_agent(user_message)
    return jsonify({'response': agent_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)