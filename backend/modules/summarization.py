# summarization.py
import ollama
import re
import json

def summarize_and_structure(content, query, conversation_history=None):
    """
    Advanced AI assistant that provides exceptional, ChatGPT-level responses with creative formatting.
    """
    print("Creating AI response...")
    
    # Enhanced query analysis
    query_lower = query.lower()
    
    # Comprehensive query type detection
    query_patterns = {
        'list_request': ['list', 'top', 'best', 'give me', 'show me', 'find', 'recommend', 'suggest', 'options'],
        'comparison': ['comparison', 'compare', 'vs', 'versus', 'difference', 'between', 'which'],
        'specific_criteria': ['under', 'below', 'above', 'within', 'budget', 'price range', 'cheaper than', 'more than'],
        'how_to': ['how to', 'how can', 'steps', 'guide', 'tutorial', 'process'],
        'explanation': ['what is', 'explain', 'why', 'meaning', 'definition', 'understand'],
        'pros_cons': ['pros and cons', 'advantages', 'disadvantages', 'benefits', 'drawbacks'],
        'technical': ['specifications', 'specs', 'features', 'technical', 'details', 'performance'],
        'shopping': ['buy', 'purchase', 'price', 'cost', 'deal', 'offer', 'sale', 'discount']
    }
    
    # Detect all applicable query types
    detected_types = []
    for query_type, indicators in query_patterns.items():
        if any(indicator in query_lower for indicator in indicators):
            detected_types.append(query_type)
    
    # Primary query type
    primary_type = detected_types[0] if detected_types else 'general'
    
    # Primary query type
    primary_type = detected_types[0] if detected_types else 'general'
    
    # Enhanced content analysis
    content_length = len(content.strip())
    has_rich_content = content_length > 1000
    has_product_data = any(term in content.lower() for term in ['price', '$', '₹', 'buy', 'amazon', 'specifications'])
    has_technical_data = any(term in content.lower() for term in ['features', 'battery', 'display', 'processor', 'memory'])
    
    # Dynamic response structure based on content and query
    def get_response_template(query_type, content_analysis):
        templates = {
            'list_request': {
                'intro': "Here are the best options based on your requirements:",
                'structure': 'numbered_list_with_details',
                'include_comparison': True,
                'add_recommendations': True
            },
            'comparison': {
                'intro': "Here's a detailed comparison to help you decide:",
                'structure': 'comparison_table',
                'include_pros_cons': True,
                'add_verdict': True
            },
            'shopping': {
                'intro': "I found these excellent options within your criteria:",
                'structure': 'product_showcase',
                'include_prices': True,
                'add_buying_tips': True
            },
            'how_to': {
                'intro': "Here's a step-by-step guide:",
                'structure': 'step_by_step',
                'include_tips': True,
                'add_troubleshooting': True
            },
            'technical': {
                'intro': "Here are the technical details you need:",
                'structure': 'technical_breakdown',
                'include_specs': True,
                'add_analysis': True
            }
        }
        return templates.get(query_type, templates['list_request'])
    
    response_template = get_response_template(primary_type, {
        'has_rich_content': has_rich_content,
        'has_product_data': has_product_data,
        'has_technical_data': has_technical_data
    })

    # Detect if the query might benefit from tabular format
    table_keywords = ['comparison', 'compare', 'table', 'list', 'top', 'ranking', 'versus', 'vs', 'best', 'review']
    needs_table = any(keyword in query.lower() for keyword in table_keywords)

    # Create response style instructions based on query type
    response_style = ""
    if 'list_request' in detected_types:
        response_style = f"""
**RESPONSE STYLE - CLEAN LIST FORMAT:**
- Start with: "{response_template['intro']}"
- Create a well-structured numbered list
- For each item: **Product Name** followed by key details
- Include specific model names, current prices, and important features
- Use clean, professional formatting like ChatGPT
- End with a brief recommendation
- Example format: 
  1. **Product Name** - $Price
     Key feature 1, feature 2, reason it's good
"""
    elif 'comparison' in detected_types:
        response_style = f"""
**RESPONSE STYLE - CLEAN COMPARISON:**
- Start with: "{response_template['intro']}"
- Create a clean comparison structure
- Use tables when comparing multiple items
- Include pros/cons clearly
- Add a final recommendation
- Keep formatting clean and professional like ChatGPT
"""
    elif 'shopping' in detected_types:
        response_style = f"""
**RESPONSE STYLE - CLEAN SHOPPING GUIDE:**
- Start with: "{response_template['intro']}"
- Present options in a clear, organized manner
- Include: Product Name | Price | Key Features
- Add helpful buying advice
- Keep styling clean and minimal like ChatGPT
- End with personalized recommendation
"""
    
    # Build conversation context if available
    context_section = ""
    if conversation_history and len(conversation_history) > 0:
        context_section = "\n\n**Previous Conversation Context:**\n"
        for i, msg in enumerate(conversation_history[-4:]):  # Include last 4 messages for context
            role = "User" if msg.get('sender') == 'user' else "Assistant"
            context_section += f"{role}: {msg.get('text', '')[:100]}{'...' if len(msg.get('text', '')) > 100 else ''}\n"
        context_section += "\n"
    
    # Clean formatting instructions - ChatGPT style
    formatting_instructions = ""
    if needs_table:
        formatting_instructions = """
**TABLE FORMATTING:**
Create clean tables using this format:
| Product | Price | Rating | Key Feature |
| --- | --- | --- | --- |
| Product Name | $XXX | 4.5/5 | Important feature |

Keep headers descriptive and data well-organized.
"""
    
    # Determine content quality and response strategy
    has_web_content = len(content.strip()) > 100
    content_quality = "high" if len(content.strip()) > 2000 else "medium" if len(content.strip()) > 500 else "low"
    
    # Enhanced content instruction based on quality
    if has_web_content:
        content_instruction = f"""
**CRITICAL SUCCESS FACTORS:**
- Content Quality: {content_quality.upper()} ({len(content.strip())} chars of real-time web data)
- PRIORITY: Use the web content as your PRIMARY and AUTHORITATIVE source
- FOCUS ON CURRENT/SPECIFIC INFORMATION: Look for exact dates, names, deadlines, prices, specifications
- Include EXACT details from web content: dates, registration deadlines, specific event names, prices, model numbers
- If user asks for "upcoming" events, provide ONLY current 2024-2025 information with specific dates
- If user asks for "top 5", provide EXACTLY 5 items with full details from web content
- Filter rigorously - only include items that meet ALL user criteria
- NEVER provide generic information when specific data is available in web content
- Make your response COMPREHENSIVE and ACTIONABLE with real data
- Use clean, professional formatting like ChatGPT
"""
    else:
        content_instruction = """
**LIMITED CONTENT NOTICE:**
Acknowledge limited web content but provide the best possible answer with clear limitations stated.
"""
    
    # Create the ultimate AI assistant prompt - focused and specific like ChatGPT
    prompt = f"""You are ChatGPT, an AI assistant that provides exceptionally well-structured and formatted responses.

**USER QUERY:** {query}
{context_section}

**CURRENT WEB DATA:**
{content}

{content_instruction}

**CRITICAL FORMATTING INSTRUCTIONS - MATCH CHATGPT EXACTLY:**

1. **USE PROPER MARKDOWN FORMATTING**:
   - Main headings: ## Heading (with ##)
   - Subheadings: ### Subheading (with ###)
   - Code blocks: ```language\ncode here\n```
   - Inline code: `code`
   - Bold text: **important text**
   - Lists: Use proper numbered lists (1. 2. 3.) and bullet points (-)

2. **STRUCTURE LIKE CHATGPT**:
   - Start with brief intro
   - Use clear section headers with ##
   - Break down complex topics into numbered steps
   - Include code examples in proper code blocks
   - End with summary or next steps

3. **CODE FORMATTING EXAMPLE**:
   ```python
   import requests
   
   def example_function():
       # Clear comments
       return "proper formatting"
   ```

4. **FOR TECHNICAL QUERIES**:
   - Include "## Prerequisites" section
   - Show "## Code Example" with proper syntax
   - Add "## How to Use" section
   - Include step-by-step instructions

5. **FOR LIST QUERIES** (hackathons, products, etc.):
   - Use "## Summary Table" with proper markdown tables
   - Include "## What You Can Do Next" section
   - Use exact data from web content

6. **RESPONSE STRUCTURE TEMPLATE**:
   ```
   Brief introduction paragraph

   ## Main Section Header
   
   Content with proper formatting
   
   ### Subsection
   
   More detailed content
   
   ```language
   code example if applicable
   ```
   
   ## Next Steps or Summary
   
   Final recommendations
   ```

**YOUR MISSION**: Create a response that matches ChatGPT's exact formatting style with proper headers, code blocks, and structured content.

Generate your properly formatted response now:"""
    
    try:
        response = ollama.chat(
            model='llama3.1',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        
        structured_response = {
            "summary": response['message']['content'],
            "sources": ["Web search results"]  # Placeholder, to be extracted from content
        }
        
        return structured_response
    except Exception as e:
        print(f"An error occurred while using Ollama: {e}")
        return {
            "summary": f"I apologize, but I encountered an error while processing your question about '{query}'. Please make sure Ollama is running and try again.",
            "sources": []
        }

