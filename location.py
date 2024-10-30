import random
from helper import country_dict
from difflib import SequenceMatcher
import api

class Location:
    def __init__(self, city, country):
        self.city = city
        self.country = country 


    @staticmethod
    def create_location():
        country = random.choice(list(country_dict.keys()))
        city = api.get_random_city(country)

        if(api.create_street_view_image(city)):
            return Location(city, country)
        else:
            return Location.create_location()

    def generate_fact(self, params):
        category, difficulty = params
        country = country_dict[self.country][0]
        prompt = f"give me a fact about the country {country} in this category: {category}, in the format 'this country ...', dont say the name of the country in the fact, the difficulty of this fact should be {difficulty}, the fact should ONLY be in THIS CATEGORY: '{category}', make sure that you dont say the name of the country in the response."
        
        print('Generating hint...')
        fact = api.prompt_ollama(prompt)

        return fact

    def match_country_string(self, string):
        for idx, synonym in enumerate(country_dict[self.country]):
            if (SequenceMatcher(None, string, synonym).ratio() > 0.8):
                return True

        return False