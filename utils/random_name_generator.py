import random
import string

def generate_random_name():
    name_length = random.randint(5, 7)  # Generate a random length between 5 and 7 characters
    name = ''.join(random.choice(string.ascii_letters) for _ in range(name_length))
    return name