# web_search.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse

def fallback_search(query, num_results=10):
    """
    Fallback search method using requests and BeautifulSoup
    """
    try:
        print(f"Fallback search for: {query}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Clean and encode the search query
        clean_query = query.strip()
        if not clean_query:
            print("Empty query provided")
            return []
            
        encoded_query = urllib.parse.quote_plus(f"{clean_query} 2024 2025")
        search_url = f"https://www.google.com/search?q={encoded_query}&num=20&hl=en"
        
        print(f"Search URL: {search_url}")
        
        response = requests.get(search_url, headers=headers, timeout=15)
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Bad response status: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        
        # Try multiple search result selectors
        selectors = [
            'div.g a[href]',
            'div.yuRUbf a[href]',
            'h3 a[href]',
            'a[href*="/url?q="]',
            'a[data-ved][href]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            print(f"Selector '{selector}' found {len(elements)} elements")
            
            for element in elements:
                if len(links) >= num_results:
                    break
                    
                href = element.get('href', '')
                
                if href.startswith('/url?q='):
                    # Extract the actual URL from Google's redirect
                    try:
                        actual_url = href.split('/url?q=')[1].split('&')[0]
                        actual_url = urllib.parse.unquote(actual_url)
                    except:
                        continue
                elif href.startswith('http'):
                    actual_url = href
                else:
                    continue
                
                # Filter valid URLs
                if (actual_url.startswith('http') and 
                    'google.com' not in actual_url and 
                    'youtube.com' not in actual_url and
                    'googleusercontent.com' not in actual_url and
                    actual_url not in links):
                    links.append(actual_url)
                    print(f"Added URL: {actual_url}")
            
            if links:  # If we found some links, break
                break
        
        print(f"Fallback search found {len(links)} URLs")
        
        # If no links found, try some reliable sources based on query content
        if not links:
            print("No links found, trying reliable sources...")
            reliable_urls = get_reliable_urls_for_query(query)
            links.extend(reliable_urls)
        
        return links[:num_results]
        
    except Exception as e:
        print(f"Fallback search failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        # Last resort: return some reliable URLs based on query
        try:
            reliable_urls = get_reliable_urls_for_query(query)
            print(f"Using reliable URLs as last resort: {len(reliable_urls)} URLs")
            return reliable_urls[:num_results]
        except:
            return []

def get_reliable_urls_for_query(query):
    """Get some reliable URLs based on query content"""
    query_lower = query.lower()
    urls = []
    
    # Tech/gadget queries
    if any(word in query_lower for word in ['laptop', 'phone', 'smartwatch', 'gadget', 'tech', 'review']):
        urls.extend([
            'https://www.gadgets360.com/',
            'https://www.91mobiles.com/',
            'https://www.smartprix.com/',
            'https://www.flipkart.com/',
            'https://www.amazon.in/'
        ])
    
    # Hackathon/coding queries
    if any(word in query_lower for word in ['hackathon', 'coding', 'programming', 'competition']):
        urls.extend([
            'https://unstop.com/hackathons',
            'https://www.hackerearth.com/challenges/',
            'https://mlh.io/',
            'https://devpost.com/',
            'https://github.com/avinash201199/Competitions-and-Programs-List'
        ])
    
    # General tech/news queries
    if any(word in query_lower for word in ['news', 'latest', 'update', 'announcement']):
        urls.extend([
            'https://techcrunch.com/',
            'https://www.theverge.com/',
            'https://arstechnica.com/',
            'https://www.wired.com/'
        ])
    
    # Programming/development queries
    if any(word in query_lower for word in ['code', 'api', 'development', 'programming', 'tutorial']):
        urls.extend([
            'https://stackoverflow.com/',
            'https://github.com/',
            'https://developer.mozilla.org/',
            'https://docs.python.org/',
            'https://medium.com/'
        ])
    
    # If no specific category, add some general reliable sources
    if not urls:
        urls.extend([
            'https://www.wikipedia.org/',
            'https://stackoverflow.com/',
            'https://medium.com/',
            'https://github.com/',
            'https://news.ycombinator.com/'
        ])
    
    return urls[:10]

def search_web(keywords, num_results=10):
    """
    Searches Google for the given keywords and returns the top N search result URLs.
    """
    print(f"Searching web for: {keywords}")
    
    # First try fallback method (more reliable)
    if isinstance(keywords, list):
        query = " ".join([str(k) for k in keywords if k])
    else:
        query = str(keywords)
    
    print(f"Trying fallback search first...")
    fallback_links = fallback_search(query, num_results)
    if fallback_links:
        print(f"Fallback found {len(fallback_links)} URLs")
        print(f"Found URLs: {fallback_links[:5]}")  # Show first 5 URLs for debugging
        return fallback_links
    
    print(f"Fallback failed, trying Selenium...")
    
    try:
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Create a more intelligent search query
        if isinstance(keywords, list):
            # Combine keywords intelligently
            query = " ".join(keywords)
        else:
            query = keywords
            
        # Add current year and specific search terms for better results
        current_year = "2024 2025"
        
        # Enhance search query based on content type for much better results
        query_lower = query.lower()
        if 'hackathon' in query_lower:
            # Use the first, most specific query for hackathons
            search_query = f"{query} {current_year} registration dates india students"
        elif any(word in query_lower for word in ['smartwatch', 'phone', 'laptop', 'gadget']):
            search_query = f"{query} {current_year} price specifications review"
        elif any(word in query_lower for word in ['upcoming', 'events', 'conference']):
            search_query = f"{query} {current_year} schedule dates registration"
        elif any(word in query_lower for word in ['price', 'cost', 'under']):
            search_query = f"{query} {current_year} price list specifications"
        else:
            search_query = f"{query} {current_year}"
        
        print(f"Search query: {search_query}")
        
        # Perform search
        search_url = f"https://www.google.com/search?q={search_query}&num=20"
        driver.get(search_url)
        
        # Wait for results to load
        time.sleep(2)
        
        # Try different CSS selectors for Google search results
        selectors = [
            'div.g a[href]',
            'div.yuRUbf a[href]', 
            'h3.LC20lb a[href]',
            'a[href][data-ved]'
        ]
        
        # Filter out sites known to block scrapers and prioritize scraper-friendly sites
        links = []
        friendly_sites = []
        other_sites = []
        
        # Sites that are generally more scraper-friendly
        scraper_friendly_domains = [
            'croma.com', 'amazon.', 'flipkart.', 'myntra.', 'ajio.', 'nykaa.',
            'techcrunch.', 'gadgets360.', '91mobiles.', 'smartprix.', 'beebom.',
            'indianexpress.', 'hindustantimes.', 'timesofindia.', 'ndtv.',
            'moneycontrol.', 'livemint.', 'businesstoday.', 'financialexpress.',
            'ibm.com', 'microsoft.com', 'aws.amazon.com', 'cloud.google.',
            'blog.', 'medium.', 'linkedin.', 'github.com', 'stackoverflow.'
        ]
        
        # Sites that commonly block scrapers
        blocking_domains = [
            'wikipedia.org', 'pcmag.com', 'theverge.com', 'wired.com',
            'techradar.com', 'cnet.com', 'engadget.com', 'ars-technica.com'
        ]
        
        for selector in selectors:
            try:
                link_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in link_elements:
                    if len(friendly_sites) + len(other_sites) >= num_results:
                        break
                    try:
                        href = element.get_attribute('href')
                        if (href and href.startswith('http') and 
                            'google.com' not in href and 
                            'youtube.com' not in href):
                            
                            # Check if domain is scraper-friendly
                            is_friendly = any(domain in href for domain in scraper_friendly_domains)
                            is_blocking = any(domain in href for domain in blocking_domains)
                            
                            if not is_blocking and href not in [item[1] for item in friendly_sites + other_sites]:
                                if is_friendly:
                                    friendly_sites.append((element.text or href, href))
                                else:
                                    other_sites.append((element.text or href, href))
                                    
                    except Exception as e:
                        continue
                
                if len(friendly_sites) + len(other_sites) >= num_results:
                    break
                    
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
                continue
        
        # Prioritize friendly sites, then add others
        all_sites = friendly_sites + other_sites
        links = [href for _, href in all_sites[:num_results]]
                
        driver.quit()
        
        print(f"Found {len(links)} URLs")
        return links
        
    except Exception as e:
        print(f"Web search error, trying fallback...")
        
        # Try fallback search method
        if isinstance(keywords, list):
            query = " ".join(keywords)
        else:
            query = keywords
            
        fallback_links = fallback_search(query, num_results)
        print(f"Fallback found {len(fallback_links)} URLs")
        return fallback_links

