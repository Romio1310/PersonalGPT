# query_understanding.py
import spacy

# Load the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_keywords(query):
    """
    Enhanced keyword extraction for better search results and current information
    """
    print(f"Extracting keywords from: {query}")
    
    # Load spacy model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    
    # Extract meaningful tokens (nouns, proper nouns, adjectives, and verbs)
    keywords = []
    for token in doc:
        # Include important words and filter out stop words, punctuation
        if (token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'VERB'] and 
            not token.is_stop and 
            not token.is_punct and 
            len(token.text) > 2):
            keywords.append(token.text.lower())
    
    # Add specific domain keywords based on query context
    query_lower = query.lower()
    
    # Enhanced time-specific keywords for current/upcoming events
    if any(word in query_lower for word in ['upcoming', 'current', '2025', 'this year', 'next']):
        keywords.extend(['2025', '2024', 'upcoming', 'current', 'latest', 'september', 'october', 'november', 'december'])
    
    # Enhanced domain-specific keywords for hackathons
    if 'hackathon' in query_lower:
        keywords.extend([
            'hackathon', 'coding competition', 'programming contest', '2025', 'registration', 
            'dates', 'deadline', 'student hackathon', 'tech competition', 'coding event',
            'devpost', 'hackerearth', 'unstop', 'dare2compete', 'mlh', 'major league hacking'
        ])
    
    # Enhanced student-specific keywords
    if any(word in query_lower for word in ['student', 'cse', 'computer science', 'cs']):
        keywords.extend([
            'student', 'college', 'university', 'cse', 'computer science', 'cs students',
            'undergraduate', 'engineering students', 'tech students', 'indian students'
        ])
    
    # Enhanced product search keywords
    if any(word in query_lower for word in ['price', 'cost', 'budget', 'under', 'best', 'top']):
        keywords.extend(['price', 'cost', 'budget', 'rupees', 'dollars', 'best', 'top rated', 'review'])
    
    # Add platform-specific keywords for better search results
    if 'hackathon' in query_lower:
        keywords.extend(['devpost.com', 'hackerearth.com', 'unstop.com', 'dare2compete.com'])
    
    # Remove duplicates while preserving order
    unique_keywords = []
    for keyword in keywords:
        if keyword not in unique_keywords:
            unique_keywords.append(keyword)
    
    print(f"Extracted keywords: {unique_keywords}")
    return unique_keywords
    keywords = list(set(keywords))
    
    print(f"Extracted keywords: {keywords}")
    return keywords if keywords else query.split()

