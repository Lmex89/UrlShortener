import random
import string

letters = string.ascii_lowercase

def random_string(prefix:str = '', length:int = 10) -> str:
    return prefix + (''.join(random.choice(letters) for _ in range(length)))

def random_number(min:int = 0, max:int = 100) -> int:
    return random.randint(min, max)