import requests
import urllib.parse
from dotenv import load_dotenv
import os
import json
import random 
import math
import numpy as np
from difflib import SequenceMatcher
load_dotenv()


def get_street_view_image(lat, lng, api_key, num_images=36, size='1920x1080'):
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    headings = [i * (360 / num_images) for i in range(num_images)]

    for index, heading in enumerate(headings):
        params = {
            'size': size, 
            'location': f"{lat},{lng}", 
            'heading': heading, 
            'key': api_key
        }
        
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        response = requests.get(url)

        if response.status_code == 200:
            filename = f'street_view_image_{index}.jpg'
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as '{filename}'")
        else:
            print("Error fetching image:", response.status_code)


def req_location():
    def req():
        response = requests.get('https://hiveword.com/papi/random/locationNames', params='')
        try: _ = response.json()[0]['country']
        except: return None
        return response                

    counter = 0
    while True:
        counter += 1
        if counter == 3:
            print('REQUEST BROKEN')
            quit()
            
        response = req()
        if response:
            return response



def distance_formula_haversine(coordinates):
    
    la1, lo1 = coordinates[0]
    la2, lo2 = coordinates[1]
    
    la1 = la1 * math.pi / 180
    lo1 = lo1 * math.pi / 180
    la2 = la2 * math.pi / 180
    lo2 = lo2 * math.pi / 180
    
    deltalat = la2 - la1
    deltalon = lo2 - lo1
    
    radius = 6371
    
    a = math.sin(deltalat/2)**2 + math.cos(la1) * math.cos(la2) * math.sin(deltalon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c
    
    return distance




class Game:
    NUMBER_OF_ROUNDS = 5
    MAX_POINTS = 100
    MIN_POINTS = 10
    NUMBER_OF_GUESSES = 3
    NUMBER_OF_HINTS = 5

    def __init__(self, rounds=NUMBER_OF_ROUNDS):
        self.rounds = rounds
        self.round = 1
        self.points = 0
        self.started = False
        
        self.categorys = ['language', 'famous people', 'history', 'acheivments', 'flag', 'location', 'traditions', 'sport', 'cuisine', 'population', 'capital city', 'fun fact']
        self.difficultys = ['very easy', 'easy', 'medium', 'hard']

        self.state = GameState()


    def create_location(self):
        data = req_location().json()
        city = data[0]['name']
        country = data[0]['country']
        return Location(city, country)
       
    
    def hint_params(self, hints):
        cat = random.choice(self.categorys)
        diff = self.difficultys[np.clip(hints, 0, 4) - 1]
        return cat, diff


    def run(self):
        if(self.started): return
        self.started = True

        for _ in range(self.rounds):
            self.question_loop()
            self.points += self.state.points
            self.round += 1
            
        print(f'You got {self.points}!!!')
        self.started = False

    def get_answer(self):
        answer = input("Answer: ")
        print()
        try:
            return answer
        except:
            return None
        
    def __process_answer(self):
        location = self.state.location
        answer = self.state.answer
        
        if(location.match_country_string(answer)):
            return True
        
        self.state.points -= self.MAX_POINTS / self.NUMBER_OF_HINTS
        if(self.state.points < self.MIN_POINTS):
            self.state.points = self.MIN_POINTS

        if(answer != "skip"):
            print("Wrong answer!")
            self.state.guesses_left -= 1

            coordinates = [Location.get_coordinates(location.country), Location.get_coordinates(answer)]
            if None not in coordinates:
                distance = distance_formula_haversine(coordinates)
                print(f'You are {round(distance)}km away')
        
        return False
    
    def __show_hint(self):
        location = self.state.location
        hint = location.generate_fact(self.hint_params(self.state.hints_left))['response']
        if location.country in hint:
            hint = hint.replace(location.country, '______')
        
        print(hint)

    def __show_info(self):
        print(f"City: {self.state.location.city}")
        if(self.state.points < self.MAX_POINTS and self.state.hints_left > 0):
            self.__show_hint()
            self.state.hints_left -= 1
        print(f'Hints left: {self.state.hints_left}')
        print(f"Guesses left: {self.state.guesses_left}")

    def question_loop(self):
        self.state.reset()
        self.state.location = self.create_location()
        print("What country is this?")

        while True:
            if self.state.guesses_left <= 0:
                self.state.points = 0
                break
                
            self.__show_info()
            self.state.answer = self.get_answer()
            if(self.__process_answer()):
                break
                
            
        print(f'The country was {self.state.location.country}')
        print(f"You got {self.state.points} points\n\n")

class GameState:
    def __init__(self):
        self.points = Game.MAX_POINTS
        self.guesses_left = Game.NUMBER_OF_GUESSES
        self.hints_left = Game.NUMBER_OF_HINTS
        self.answer = None
        self.location = None

    def reset(self):
        self.points = Game.MAX_POINTS
        self.guesses_left = Game.NUMBER_OF_GUESSES
        self.hints_left = Game.NUMBER_OF_HINTS

class Location:
    def __init__(self, city, country):
        self.city = city
        self.country = country    
        
    @staticmethod
    def get_coordinates(place):
        api_key = os.getenv('API_KEY')
        resp = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}')

        if resp.status_code==200:
            if(resp.json()['status'] == 'OK'):
                data = resp.json()['results'][0]['geometry']['location']
                return data['lat'], data['lng']
        
        return None

    def generate_fact(self, params):
        category, difficulty = params
        url = 'http://localhost:11434/api/generate' 
        print(category)
        data = {"model": "llama3.2","prompt": f'give me a fact about the country {self.country} in this category: {category}, in the format "this country ...", dont say the name of the country in the fact, the difficulty of this fact should be {difficulty}, the fact should ONLY be in THIS CATEGORY: "{category}", make sure that you dont say the name of the country in the response.', 'stream':False} 
        print('Generating hint...')
        resp = requests.post(url, json=data).json()
        return resp

    def match_country_string(self, string):
        if (SequenceMatcher(None, string, self.country).ratio() > 0.8):
            return True

        return False

if __name__ == "__main__":
    g = Game()
    g.run()