#!/usr/bin/env python3

import sys
sys.path.append('/Users/codname_gd/Desktop/Personal_Copilot/backend')

from modules.web_search import search_web
from modules.query_understanding import extract_keywords

# Test the search functionality
query = "latest iPhone 16 features and price 2024"
print(f"Testing query: {query}")

# Test keyword extraction
keywords = extract_keywords(query)
print(f"Extracted keywords: {keywords}")

# Test web search
urls = search_web(keywords)
print(f"Found URLs: {urls}")
print(f"Number of URLs: {len(urls)}")
