import httpx
from typing import Optional
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List, Dict, Any
import spacy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


print("Loading spaCy NER model...")

print("Loading spaCy NER model...")
nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])

nlp.add_pipe("sentencizer") 
print("spaCy model and sentencizer loaded successfully.")

print("spaCy model loaded successfully.")

geolocator = Nominatim(user_agent="geo_ai_visualizer_app/1.0")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def _format_to_geopoint(name: str, city: str, entity_type: str, lat: float, lon: float) -> Dict[str, Any]:
    """Converts found data to our generic GeoJSON-like format."""
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "place_name": name.strip(),    
            "city": city.strip(),
            "entity_type": entity_type     
        }
    }

def _scrape_page_content(url: str) -> str:
    """Fetches and extracts clean text from a single webpage."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        return " ".join(soup.stripped_strings)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""


def _extract_entities_with_ner(text: str) -> List[Dict[str, str]]:
    """
    Uses spaCy NER to find places and their locations, with filtering for noise.
    """
    STOP_WORDS = {
        "Startups", "Biotech", "EdTech", "Apps", "Logistics", "Lending",
        "Crowdfunding", "Cycling", "Handmade", "Startups", "India", "USA",
        "Canada", "Singapore", "Hong Kong", "UAE", "UK", "LinkedIn", "Citi"
    }
    
    TARGET_PLACE_LABELS = {"ORG", "FAC", "LOC"}
    
    doc = nlp(text)
    found_items = []
    
    for sent in doc.sents:
        sent_places = [ent for ent in sent.ents if ent.label_ in TARGET_PLACE_LABELS]
        sent_gpes = [ent for ent in sent.ents if ent.label_ == "GPE"]
        
        if sent_places and sent_gpes:
            for place in sent_places:
                for gpe in sent_gpes:
                    
                    if place.text in STOP_WORDS or gpe.text in STOP_WORDS:
                        continue
                    
                    if len(place.text) > 2 and len(gpe.text) > 2:
                        found_items.append({
                            "name": place.text,
                            "city": gpe.text,
                            "type": place.label_
                        })
    
    return [dict(t) for t in {tuple(d.items()) for d in found_items}]

def search_and_scrape(search_topic: str, geographic_context: Optional[str] = None) -> List[Dict[str, Any]]:
    print(f"Executing Universal Entity search for: '{search_topic}', Context: '{geographic_context}'")
    geopoints = []
    geocoding_cache = {}
    
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(search_topic, region='wt-wt', max_results=3))
        
        for result in search_results:
            print(f"-> Processing: {result['href']}")
            page_text = _scrape_page_content(result['href'])
            if page_text:
                found_items = _extract_entities_with_ner(page_text)
                print(f"  - NER found {len(found_items)} potential place/location pairs.")
                
                for item in found_items:
                    city_name = item['city']
                    if city_name not in geocoding_cache:
                        location = geocode(city_name)
                        geocoding_cache[city_name] = location
                    else:
                        location = geocoding_cache[city_name]

                    if location:
                        add_item = False
                        if geographic_context:
                            if geographic_context.lower() in location.address.lower():
                                add_item = True
                                print(f"      ✓ Match! '{location.address}' is in context '{geographic_context}'. Adding.")
                            else:
                                print(f"      ✗ Filtered out. '{location.address}' is not in context '{geographic_context}'.")
                        else:
                            add_item = True

                        if add_item:
                            geopoints.append(
                                _format_to_geopoint(
                                    item['name'], city_name, item['type'],
                                    location.latitude, location.longitude
                                )
                            )
    
        final_list = []
        seen = set()
        for gp in geopoints:
            identifier = (gp['properties']['place_name'], gp['properties']['city'])
            if identifier not in seen:
                seen.add(identifier)
                final_list.append(gp)

        print(f"Successfully generated {len(final_list)} unique geopoints after filtering.")
        return final_list

    except Exception as e:
        print(f"An error occurred in the main search/scrape loop: {e}")
        return []