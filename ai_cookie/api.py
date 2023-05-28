import openai

from secrets import OPENAI_KEY

openai.api_key = OPENAI_KEY

def whisper(path: str) -> str:
    """Basic transcription from filepath."""
    transcript = openai.Audio.translate(
        "whisper-1", 
        open(path, 'rb'), 
        options = {
                    "language" : "en",
                    "temperature" : "0"
                    }
                )
    return transcript.text
    
    
def chatgpt(prompt: str) -> str:
    """Basic ChatGPT prompt only."""
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    raw_commands = completion.choices[0].message.content
    return raw_commands
        
