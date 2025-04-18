from flask import Flask, request, jsonify
from agent import run_agent
import json

app = Flask(__name__)

@app.route('/api/run', methods=['POST'])
def run_engine():
    data = json.loads(request.data)
    print(data)
    query = data.get('query')
    context = data.get('context')

    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400

    # Run the agent with the provided query and context
    result = run_agent(query,context)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
