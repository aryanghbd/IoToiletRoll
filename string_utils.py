import random
#String utils for SMS strings
#Simply generate custom SMS boiler plate strings based on use and random selection, using clauses.

def generate_output_string(name, number):
    greetings = ["What's up, ", "How's it hanging, or should I say... how's it rolling, ", "Greetings from the toilet, ", "All done, ", "Nice flush, "]
    greeting = random.choice(greetings)
    return greeting + name + f". You rolled {number} times this session, taking approximately {number*2} sheets by our estimates."

def generate_custom_string(number):
    if 1 <= number <= 3:
        return " Very efficient usage! Keep going to keep the environment rolling as well as you are!"
    if 4 <= number <= 10:
        return " Nice usage! Keep up the moderate usage to help the environment one toilet trip at a time."
    if 11 <= number <= 25:
        return " Are you flushing down a textbook? At " + str(number * 0.12) + "m, you rolled a small child or a baseball bat, do better."
    if 26 <= number <= 40:
        return " God damn."
    else:
        return " Roll with awareness!"