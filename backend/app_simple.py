from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get('query')
    conversation_history = data.get('conversation_history', [])

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    # Simple response for testing
    result = {
        "summary": f"**Test Response**\n\nYou asked: {query}\n\nThis is a simple test response. The full AI pipeline requires fixing the numpy/spacy compatibility issue.\n\n**Your Query:**\n- {query}\n\n**Conversation History:**\n- {len(conversation_history)} previous messages",
        "sources": []
    }
    
    return jsonify(result)

if __name__ == "__main__":
    print("=" * 60)
    print("Personal AI Copilot - Simple Test Server")
    print("=" * 60)
    print("Server running on http://localhost:5001")
    print("Waiting for requests...")
    print("=" * 60)
    app.run(debug=True, port=5001)
