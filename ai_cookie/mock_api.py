import random

options = ['isnt this lovely', 'what a nice day', 'leo on the plane', 'lets stop now']


def whisper(path: str) -> str:
    return random.choice(options)
    
    
def chatgpt(prompt: str) -> str:
    """Basic ChatGPT prompt only."""
    return random.choice(options)        
