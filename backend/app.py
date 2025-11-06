from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.query_understanding import extract_keywords
from modules.web_search import search_web
from modules.content_scraping import scrape_content
from modules.pre_filtering import filter_content
from modules.summarization import summarize_and_structure

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def main_pipeline(query, conversation_history=None):
    """
    Main pipeline for the AI Copilot.
    """
    print(f"Received query: {query}")
    if conversation_history:
        print(f"Conversation history: {len(conversation_history)} messages")

    # 1. Query Understanding
    keywords = extract_keywords(query)
    print(f"Extracted keywords: {keywords}")

    # 2. Web Search
    urls = search_web(keywords)
    print(f"Found URLs: {urls}")

    # 3. Scrape Content
    scraped_content = scrape_content(urls)
    print(f"Scraped content length: {len(scraped_content)} characters")

    # 4. Pre-filtering
    filtered_content = filter_content(scraped_content, keywords)
    print(f"Filtered content length: {len(filtered_content)} characters")

    # 5. Summarize and Structure - Pass the original query and conversation history
    result = summarize_and_structure(filtered_content, query, conversation_history)

    print("Final Result:")
    print(result)
    return result

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get('query')
    conversation_history = data.get('conversation_history', [])

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    result = main_pipeline(query, conversation_history)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

