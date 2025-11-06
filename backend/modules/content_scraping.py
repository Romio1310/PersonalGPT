# content_scraping.py
import requests
from bs4 import BeautifulSoup
import trafilatura
import time
import random

def scrape_content(urls):
    """
    Scrapes the main content from a list of URLs with anti-blocking measures.
    """
    print(f"Scraping content from {len(urls)} URLs...")
    
    all_content = []
    
    # Better headers to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    for i, url in enumerate(urls):
        try:
            # Add random delay to avoid rate limiting
            if i > 0:
                time.sleep(random.uniform(0.5, 1.5))
            
            # Try trafilatura first (often bypasses blocks better)
            downloaded = trafilatura.fetch_url(url, config={'DEFAULT': {'USER_AGENT': headers['User-Agent']}})
            main_content = trafilatura.extract(downloaded)
            
            if main_content and len(main_content) > 100:
                all_content.append(main_content)
            else:
                # Fallback to requests with better headers
                response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                response.raise_for_status()
                
                # Use BeautifulSoup as secondary extraction
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove unwanted elements
                for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    element.decompose()
                
                # Extract text from main content areas
                content_selectors = [
                    'article', 'main', '.content', '.post-content', 
                    '.entry-content', '.article-body', 'div[role="main"]'
                ]
                
                extracted_text = ""
                for selector in content_selectors:
                    elements = soup.select(selector)
                    if elements:
                        extracted_text = ' '.join([elem.get_text(strip=True) for elem in elements])
                        break
                
                if not extracted_text:
                    # Final fallback - get all paragraph text
                    paragraphs = soup.find_all('p')
                    extracted_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
                
                if extracted_text and len(extracted_text) > 100:
                    all_content.append(extracted_text)
                
        except requests.exceptions.Timeout:
            continue  # Skip timeouts silently
        except requests.exceptions.HTTPError as e:
            continue  # Skip HTTP errors silently
        except Exception as e:
            continue  # Skip other errors silently
            
    combined_content = "\n\n".join(all_content)
    print(f"Content scraped: {len(combined_content)} characters from {len(all_content)} sources")
    return combined_content

