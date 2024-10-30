from helper import country_dict, distance_between_coords
import random
import api
import numpy as np
from location import Location

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

        self.state = GameState(Game.MAX_POINTS, Game.NUMBER_OF_GUESSES, Game.NUMBER_OF_HINTS)
    
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

    def get_guess(self):
        guess = input("Guess: ")
        print()
        return guess
        
    def __process_guess(self):
        state = self.state
        
        if(state.location.match_country_string(state.guess)):
            return True
        
        state.points -= Game.MAX_POINTS / Game.NUMBER_OF_HINTS
        if(state.points < Game.MIN_POINTS):
            state.points = Game.MIN_POINTS

        if(state.guess != "skip"):
            state.guesses_left -= 1
            print("Wrong guess!")
            self.__show_distance_away()
        
        return False
    
    def __show_distance_away(self):
        guess_coords = api.get_coords(self.state.guess)
        answer_coords = api.get_coords(country_dict[self.state.location.country][0])

        if guess_coords is None or answer_coords is None:
            return
        
        distance = distance_between_coords(guess_coords, answer_coords)
        print(f'You are {round(distance)}km away')
    
    def __show_hint(self):
        location = self.state.location
        hint = location.generate_fact(self.hint_params(self.state.hints_left))['response']

        for i, synonym in enumerate(country_dict[location.country]):
            if synonym in hint:
                hint = hint.replace(synonym, '______')
        
        print(hint)

    def __show_info(self):
        print(f"City: {self.state.location.city}")
        if(self.state.points < self.MAX_POINTS and self.state.hints_left > 0):
            self.__show_hint()
            self.state.hints_left -= 1
        print(f'Hints left: {self.state.hints_left}')
        print(f"Guesses left: {self.state.guesses_left}")

    def question_loop(self):
        state = self.state

        state.reset()
        state.location = Location.create_location()
        print("What country is this?")

        while True:
            if state.guesses_left <= 0:
                state.points = 0
                break
                
            self.__show_info()
            state.guess = self.get_guess()
            if(self.__process_guess()):
                break
                
            
        print(f'The country was {country_dict[self.state.location.country][0]}')
        print(f"You got {self.state.points} points\n\n")

class GameState:
    def __init__(self, points, num_guesses, num_hints):
        self.start_points = points
        self.num_guesses = num_guesses
        self.num_hints = num_hints

        self.points = self.start_points
        self.guesses_left = self.num_guesses
        self.hints_left = self.num_hints
        self.guess = None
        self.location = None

    def reset(self):
        self.points = self.start_points
        self.guesses_left = self.num_guesses
        self.hints_left = self.num_hints