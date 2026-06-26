import os
import requests
import random
from bs4 import BeautifulSoup

GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')

def fetch_reviews(business_name, source='self', api_key=None):
    """
    Fetches reviews for a business.
    Tries Google Places API first, then falls back to a simple search scraper,
    and finally to mock data if all else fails.
    """
    print(f"Fetching reviews for {business_name} ({source})...")
    
    actual_api_key = api_key or GOOGLE_PLACES_API_KEY
    
    if actual_api_key:
        try:
            return fetch_from_places_api(business_name, source, actual_api_key)
        except Exception as e:
            print(f"Places API failed: {e}")
            
    try:
        reviews = fetch_from_scraper(business_name, source)
        if reviews:
            return reviews
    except Exception as e:
        print(f"Scraper failed: {e}")
        
    print("Using mock data as fallback.")
    return get_mock_reviews(business_name, source)

def fetch_from_places_api(business_name, source, api_key):
    # 1. Find Place ID
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": business_name,
        "key": api_key
    }
    resp = requests.get(search_url, params=params)
    data = resp.json()
    
    if not data.get('results'):
        raise Exception(f"No results for {business_name}")
        
    place_id = data['results'][0]['place_id']
    
    # 2. Get Details
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "reviews,name,rating",
        "key": api_key
    }
    resp = requests.get(details_url, params=params)
    data = resp.json()
    
    api_reviews = data.get('result', {}).get('reviews', [])
    
    formatted_reviews = []
    for r in api_reviews:
        formatted_reviews.append({
            "source": source,
            "business_name": business_name,
            "rating": r.get('rating', 5),
            "text": r.get('text', ""),
            "timestamp": r.get('time', "") # Unix timestamp
        })
        
    return formatted_reviews

def fetch_from_scraper(business_name, source):
    """
    A very simple scraper that extracts review snippets from Google search results.
    Highly brittle, but serves as a fallback.
    """
    url = f"https://www.google.com/search?q={business_name}+reviews"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200 or "sorry/index" in resp.url:
        return None
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = []
    
    # This selector is a guess and might change
    # Google often uses specific classes for search results
    for g in soup.find_all('div', class_='g'):
        snippet_div = g.find('div', class_='VwiC3b')
        if snippet_div and len(snippet_div.text) > 20:
            reviews.append({
                "source": source,
                "business_name": business_name,
                "rating": random.randint(3, 5), # Rating is hard to parse from snippets
                "text": snippet_div.text,
                "timestamp": None
            })
            
    return reviews[:10]

def get_mock_reviews(business_name, source):
    mock_reviews = []
    templates = [
        "Great service and friendly staff at {business_name}!",
        "I had a terrible experience here. The service was awful.",
        "Decent place, but a bit pricey for what it is.",
        "Absolutely love the {item} at {business_name}. Highly recommend!",
        "The wait time was way too long. Never coming back.",
        "Very clean and well-maintained. The staff is professional.",
        "Standard experience. Nothing special.",
    ]
    items = ["coffee", "sandwich", "consultation", "service"]
    
    for i in range(5):
        template = random.choice(templates)
        rating = random.randint(1, 5)
        text = template.format(business_name=business_name, item=random.choice(items))
        mock_reviews.append({
            "source": source,
            "business_name": business_name,
            "rating": rating,
            "text": text,
            "timestamp": None
        })
    return mock_reviews
