import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")

def check_street_view(city):
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?"
    params = {"key": {api_key}, "location": {city}}
    data = make_request(url, params).json()

    if(data["status"] != "OK"):
        return False
    
    return True

def create_street_view_image(city, size='1920x1080'):
    if(not check_street_view(city)):
        return False
    
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {'size': size, 'location': city, 'key': api_key}
        
    response = make_request(url, params)

    filename = f'street_view_image.jpg'
    with open(filename, 'wb') as f:
        f.write(response.content)

    return True

def get_coords(place):
    if(place == ""): return None
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place, "key": api_key}
    data = make_request(url, params).json()

    try: 
        data['results'][0]['geometry']['location']
    except:
        return None
    
    return data['results'][0]['geometry']['location']['lat'], data['results'][0]['geometry']['location']['lng']

def get_random_city(country):
    url = "https://hiveword.com/papi/random/locationNames"
    params = {'country': country}
    data = make_request(url, params).json()
    
    try: 
        data[0]['name']
    except: 
        return None
    
    return data[0]['name']

def prompt_ollama(prompt):
    data = {"model": "llama3.2", "prompt": prompt, "stream":False}
    url = 'http://localhost:11434/api/generate'
    response = requests.post(url, json=data)

    return response.json()

def make_request(url, params):
    response = requests.get(url, params)

    if response.status_code != 200:
        raise Exception(f"Error making request with url: {url}")

    return response