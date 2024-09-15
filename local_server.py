from flask import Flask, jsonify, request
from flask_cors import CORS
from agents.run_agents import run_agents_with_topic
import asyncio

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/generate_tweets', methods=['GET', 'OPTIONS'])
def generate_tweets():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        return '', 204
    subject = request.args.get('subject', 'World')
    tweets = asyncio.run(run_agents_with_topic(subject))
    return jsonify({"tweets": tweets})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)