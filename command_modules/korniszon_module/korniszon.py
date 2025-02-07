from utils.utilities import wait_find_input_and_send_keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
from utils.types import CommandData
from command_modules.korniszon_module.leaderboard import Leaderboard
from users import Cooldown


class Korniszon:

    def __init__(self, driver: webdriver.Chrome, leaderboard: Leaderboard):
        self.driver = driver
        self.leaderboard = leaderboard


    def check_symbol(self, symbol: str) -> str:
        vowels = "aeiouyąęóAEIOUYĄĘÓ"

        if symbol.isdigit():
            return "Number"
        elif symbol.isalpha():
            if symbol in vowels:
                return 'Vowel'
            else:
                return "Letter"
        elif symbol == " ":
            return "Space"
        
        else:
            return "Other"
        
        
    def korniszon_cleanup(self, korniszon_input):

        korniszon_input = korniszon_input.lower() # make words lowercase so they look better
        korniszon_input = korniszon_input.rstrip() # remove spaces after string, so there are no doubles counted as diffrent word with spaces at the end
        korniszon_input = ''.join([char for char in korniszon_input if char.isalpha() or char == " "]) # clear the word from anything else than letters and spaces
    
        return korniszon_input
        
        
    def score_characters_value(self, score, korniszon_input):
        for char in korniszon_input:

            if self.check_symbol(char) in ['Letter', 'Vowel', 'Space']:

                rand = random.randint(9, 15)
                char_score = ord(char) % rand
                score += char_score * 2
        
        score = score / len(korniszon_input)

        score /= 2.413 # tuning
        score *= random.uniform(1, 1.06) # grain of randomness
        score *= 10 # to make it look nicer

        return round(score, 2)


    def score_vowels_percent(self, score, korniszon_input):

        target_vowels_percent = 33

        vowels_count = 0
        vowels_percent = 0
        word_lenght = len(korniszon_input.replace(" ", "")) # so it doesn't count spaces

        for char in korniszon_input:
            if self.check_symbol(char) == 'Vowel':
                vowels_count += 1

        # calculate the percentage of vowels in the input word
        vowels_percent = vowels_count / word_lenght * 100
            # print(f"Vowels percent: {vowels_percent} = {vowels_count} / {word_lenght} * 100 ")

        # remove all decimals to make it more predictable for testing etc
        vowels_percent = int(vowels_percent)

        # calculate the diffrence between the desired percentage and the actual percentage 
        diffrence = target_vowels_percent - vowels_percent
            # print(f"Diffrence: {diffrence} = {target_vowels_percent} - {vowels_percent}")

        # then how much to subtract from the best mutliplier (which is *2)
        # we want around 30% of vowels in the word, which subtracts 0
        # the closer to 0% or 100%, the worse the subtraction. Up to 2.
        # That's why we are dividing the diffrence by 16.5 or 33.5 (for target 33) to get the subtraction in the range of 0-2, from the best to the worst

        # we are looking for a number which, if you divide diffrence by it, will give you a number from 0 to 2
        divide_positive = target_vowels_percent / 2 # 16.5 if target is 33 etc
        divide_negative = (target_vowels_percent - 100) / 2 # 33.5 if target is 33 etc

        multiplier_subtract = 0
        # up to 33
        if diffrence > 0:
            multiplier_subtract = abs(diffrence / divide_positive)

        # down to -67
        elif diffrence < 0:
            multiplier_subtract = abs(diffrence / divide_negative)


        # now i'm subtracting the best multiplier (2) by above result
        base_multiplier = 2
        vowels_multiplier = base_multiplier - round(multiplier_subtract, 2)
            # print(f"Multiplier: {vowels_multiplier} = {base_multiplier} - {diffrence}")

        # and finally apply the multiplier to the score
        print(f"Score before: {score}")
        score *= vowels_multiplier

        return round(score, 2)


    def score_repetitions(self, score, korniszon_input):

        chars_reps = []

        for char in korniszon_input:

            if char not in chars_reps:
                chars_reps.append(char)

                if self.check_symbol(char) != 'Vowel':

                    if korniszon_input.count(char) > 2: # do it only if there are alot of repetitions

                        repetitions = korniszon_input.count(char) / 2
                        score /= repetitions

                        print(f"{char}: {score} / {repetitions}")
        
        return round(score, 2)


    def score_lenght(self, score, korniszon_input):
        
        lenght = len(korniszon_input)
        rand = random.randint(5, 10)
        golden_lenght = rand # the best number of letters for a korniszon
        diffrence = abs(golden_lenght - lenght)
        diffrence_halved = diffrence / 4

        #avoid dividing by 0
        if diffrence_halved > 0:
            score /= diffrence_halved

        return round(score, 2)


    # def calculate_time(self):

    #     second_place = self.leaderboard.leaderboard[1]
        
    #     years = datetime.now().year - second_place.get('time')['year']
    #     months = datetime.now().month - second_place.get('time')['month']
    #     days = datetime.now().day - second_place.get('time')['day']
    #     hours = datetime.now().hour - second_place.get('time')['hour']
    #     minutes = datetime.now().minute - second_place.get('time')['minute']

    #     czas = ''

    #     if years > 0:
    #         czas = f"{years} lat "

    #     if months > 0:
    #         czas += f"{months} miesięcy "

    #     if days > 0:
    #         czas += f"{days} dni "

    #     if hours > 0:
    #         czas += f"{hours} godzin "

    #     if minutes > 0:
    #         czas += f"{minutes} minut "        

    #     return czas


    def send_results(self, score, korniszon_input, position):

        # special message if korniszon get top place
        if position == 1:

            response = (f"<paker>!! {korniszon_input} zdobył {score} punktów, zajął 1 miejsce i został nowym liderem rankingu!! <paker>\n")
                        # f"<paker> {input} był na szczycie przez {calculate_time(leaderboard)} <paker>")
            
        # for other positions
        else:
            emotka = ""

            if score > 500:
                emotka = "! :o"
            elif score > 300:
                emotka = "! <hura>"
            elif score > 200:
                emotka = "! :>"
            elif score > 150:
                emotka = ". ;>"
            elif score == 131.72:
                emotka = ". :))"
            elif score > 100:
                emotka = ". <myśli>"
            elif score == 21.37:
                emotka = ". <lol>"
            elif score > 75:
                emotka = ".. :/"
            elif score > 50:
                emotka = ".. <palacz>"
            elif score > 0:
                emotka = "... ;("
            elif score == 00.10:
                emotka = "... <leje>"
            elif score == 0:
                emotka = "..... <idiota>"

            response = (f"{korniszon_input} zdobył {score} punktów{emotka}\n"
            f"Zajął {position} miejsce.")

        wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)


    # def edge_cases(self, korniszon_input):

    #     # if duplicates
    #     # print(f"Korniszon: {korniszon_input} in {leaderboard.leaderboard}")
    #     if any(korniszon_input == entry["input"] for entry in self.leaderboard.leaderboard):

    #         pozycja = self.leaderboard.get_position(korniszon_input)
    #         response = f"{korniszon_input} już jest na pozycji {pozycja}. Wymyśl nowego korniszona <okok>"
    #         return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
        
    #     # edge cases
    #     # in case there were no letters in korniszon and you were left with empty variable
    #     if len(korniszon_input) == 0:

    #         response = f"{random.randint(-784545, -3456)} punktów <zniesmaczony>. Naum się w korniszony!"
    #         return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
        

    #     elif len(korniszon_input) > 30:

    #         response = "Nie będę oceniał takiego długasa <nono>"
    #         return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)    



    def cooldown_wait_responde(self, cooldown: Cooldown, korniszon_data: CommandData):
        time_left = cooldown.time_remaining()
        response = f"Poczekaj {time_left} sekund, {korniszon_data['user']} <luzik>"

        wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)

    
    # def edge_cases(self):
    #     return True


    #---------------
    # main def
    def rate_korniszon(self, korniszon_data: CommandData, cooldown: Cooldown):

        if cooldown.on_cooldown:

            self.cooldown_wait_responde(cooldown, korniszon_data)
            return
        

        if not cooldown.on_cooldown:

            score = 0

            # remove special chars, numbers etc, so it looks nice no matter how much user (fircyk) is trying to make it ugly ;>   
            # do it on korniszon_data, because we later pass it to the new_korniszon function
            korniszon_data["input"] = self.korniszon_cleanup(korniszon_data["input"])

            korniszon_input = korniszon_data["input"]

            # edge cases
            # in case if korniszon is already on leaderborad
            if any(korniszon_input == entry["input"] for entry in self.leaderboard.leaderboard):

                pozycja = self.leaderboard.get_position(korniszon_input)
                response = f"{korniszon_input} już jest na pozycji {pozycja}. Wymyśl nowego korniszona <okok>"
                return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
            

            # in case there were no letters in korniszon and you were left with empty variable
            if len(korniszon_input) == 0:

                response = f"{random.randint(-784545, -3456)} punktów <zniesmaczony>. Naum się w korniszony!"
                return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
            

            elif len(korniszon_input) > 30:

                response = "Nie będę oceniał takiego długasa <nono>"
                return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
             

            # check each character unicode number and then modulo them to get some random numbers, I want to make it hard to predict
            score = self.score_characters_value(score, korniszon_input)
            print(f"Char score: {round(score, 2)}")
            print('---')

            # check how many % of the string are vowels and then multiple the score - accoring to set rules. 
            # I don't want korniszons to have too many or too less vowels so they still sounds like words, ~30% is an golden rule.
            score = self.score_vowels_percent(score, korniszon_input)
            print(f"Vowels score: {round(score, 2)}")
            print('---')

            #score repetitions
            # check every character in a string ONCE, for how many repetitions it has and then divide the score by it
            # i don't want too many the same letters in one word to avoid fgddfdgfgfff  
            score = self.score_repetitions(score, korniszon_input)
            print(f"Reps score: {round(score, 2)}")
            print('---')

            # to avoid too short or too long words, the bigger diffrence from the ideal lenght the worse score
            score = self.score_lenght(score, korniszon_input)
            print(f"Len score: {round(score, 2)}")
            print('---')


            # add new position to leaderboard, do it after calculating score
            self.leaderboard.add_korniszon(korniszon_data, score)

            # send the message on gg how much point your korniszon earned and what position it has on leaderbord
            position = self.leaderboard.get_position(korniszon_input)


            self.send_results(score, korniszon_input, position)
            print(f"Full score: {round(score, 2)}")

        

