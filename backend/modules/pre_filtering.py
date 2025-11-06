# pre_filtering.py
import nltk
from nltk.tokenize import sent_tokenize

# Download the 'punkt' tokenizer if you haven't already
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK 'punkt' model...")
    nltk.download('punkt')

def filter_content(content, keywords):
    """
    Filters content by keeping only sentences that contain the query keywords.
    Enhanced to remove irrelevant sections and focus on core content.
    """
    print(f"Filtering content with keywords: {keywords}")
    
    if not content or not keywords:
        return ""
    
    # Remove unwanted sections first
    unwanted_patterns = [
        'FAQ', 'Frequently Asked Questions', 'Q:', 'A:', 'Question:', 'Answer:',
        'UPSC', 'exam', 'test', 'quiz', 'MCQ', 'multiple choice',
        'disclaimer', 'terms and conditions', 'privacy policy',
        'advertisement', 'sponsored', 'affiliate',
        'click here', 'learn more', 'read more', 'subscribe',
        'newsletter', 'email', 'contact us'
    ]
    
    # Filter out unwanted sections
    lines = content.split('\n')
    filtered_lines = []
    skip_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if we should skip this section
        if any(pattern.lower() in line_lower for pattern in unwanted_patterns):
            skip_section = True
            continue
        
        # Check if we've moved to a new section (might be relevant again)
        if line.strip() and not line.startswith(' ') and len(line.split()) <= 5:
            skip_section = False
        
        if not skip_section and line.strip():
            filtered_lines.append(line)
    
    content = '\n'.join(filtered_lines)
        
    sentences = sent_tokenize(content)
    
    # Create different relevance levels
    high_relevance = []
    medium_relevance = []
    
    # Convert keywords to lowercase for better matching
    keywords_lower = [kw.lower() for kw in keywords]
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Skip unwanted sentence patterns
        if any(pattern in sentence_lower for pattern in [
            'faq', 'question:', 'answer:', 'q:', 'a:', 'disclaimer', 'terms of use', 'privacy policy', 'advertisement'
        ]):
            continue
        
        # Count keyword matches
        matches = sum(1 for kw in keywords_lower if kw in sentence_lower)
        
        # Enhanced high relevance criteria - especially for events/hackathons
        high_relevance_indicators = [
            'price', 'cost', '$', '₹', 'features', 'specs', 'specifications',
            'rating', 'review', 'best', 'top', 'comparison', 'vs', 'versus',
            'model', 'brand', 'display', 'battery', 'camera', 'performance',
            # Event/hackathon specific indicators
            'date', 'dates', 'deadline', 'registration', 'apply', 'participate',
            'september', 'october', 'november', 'december', '2025', '2024',
            'hackathon', 'competition', 'event', 'challenge', 'contest',
            'student', 'cse', 'computer science', 'engineering',
            'prize', 'winner', 'grand finale', 'rounds'
        ]
        
        # High relevance: contains multiple keywords or specific indicators
        if (matches >= 2 or 
            any(indicator in sentence_lower for indicator in high_relevance_indicators)):
            high_relevance.append(sentence)
        # Medium relevance: contains at least one keyword
        elif matches >= 1:
            medium_relevance.append(sentence)
    
    # For simple explanation requests, limit content more aggressively
    query_terms = ' '.join(keywords_lower)
    if any(term in query_terms for term in ['simple', 'explain', 'basic', 'introduction']):
        # Limit to core explanatory content
        filtered_sentences = high_relevance[:10] + medium_relevance[:5]
    else:
        # Combine results, prioritizing high relevance
        filtered_sentences = high_relevance + medium_relevance[:20]
    
    result = " ".join(filtered_sentences)
    print(f"Filtered content length: {len(result)} characters")
    
    return result

