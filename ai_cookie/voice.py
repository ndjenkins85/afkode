try:
    import console
    from objc_util import *
    import speech
    import sound
except:
    pass
import threading
import time

import os
import shutil
from pathlib import Path

import openai

from secrets import OPENAI_KEY

openai.api_key = OPENAI_KEY
debug = True
detected_stop_word = 'stop'
stop_threads = False
THREADS = 2
RECORD_TIME = 8

def clear_temp_directories(THREADS):
    """Clear temporary directories."""
    for i in range(THREADS):
        try:
            shutil.rmtree(f"../data/thread{i+1}")
            shutil.rmtree(f"../data/thread{i+1}_out") 
        except FileNotFoundError:
            # If the directory doesn't exist, we can just move on
            pass


def send_to_api(path):
    transcript = openai.Audio.translate(
        "whisper-1", 
        open(path, 'rb'), 
        options = {
                    "language" : "en",
                    "temperature" : "0"
                    }
                )
    return transcript.text

    
def iphone_bluetooth_record(file_name):
    global stop_threads
    """Use iphone bluetooth audio for recording."""
    AVAudioSession = ObjCClass('AVAudioSession')
    NSURL = ObjCClass('NSURL')
    AVAudioRecorder = ObjCClass('AVAudioRecorder')
    shared_session = AVAudioSession.sharedInstance()
    category_set = shared_session.setCategory_withOptions_error_(ns('AVAudioSessionCategoryPlayAndRecord'), 4, None)

    settings = {
        ns('AVFormatIDKey'): ns(1633772320),
        ns('AVSampleRateKey'):ns(16000.0),
        ns('AVNumberOfChannelsKey'):ns(1)
    }
    output_path = os.path.abspath(file_name)
    out_url = NSURL.fileURLWithPath_(ns(output_path))
    recorder = AVAudioRecorder.alloc().initWithURL_settings_error_(out_url, settings, None)
    if recorder is None:
        console.alert('Failed to initialize recorder')
        return None
    recorder.record()
    for i in range(RECORD_TIME*4):
        time.sleep(0.25)
        if stop_threads:
            return None
    recorder.stop()
    recorder.release()


def record_audio(thread_number, delay):
    """Function for recording threads."""
    global stop_threads

    # Make sure the thread's directory exists
    directory = f'../data/thread{thread_number}'
    os.makedirs(directory, exist_ok=True)

    # Count the number of files already in the directory
    file_number = len(os.listdir(directory))

    # Start with a delay
    time.sleep(delay)

    while not stop_threads:
        # File path for this recording
        padded_number = str(file_number).zfill(4)
        file_path = os.path.join(directory, f'recording{padded_number}.m4a')
        iphone_bluetooth_record(file_path)
        file_number += 1

# The function for transcription threads
def transcribe_audio(thread_number):
    global stop_threads

    # Directories for this thread's recordings and transcriptions
    input_directory = f'../data/thread{thread_number}'
    output_directory = f'../data/thread{thread_number}_out'
    os.makedirs(output_directory, exist_ok=True)

    while not stop_threads:
        # Get the list of input files and output files
        input_files = sorted(os.listdir(input_directory))
        output_files = os.listdir(output_directory)
        
        # Don't analyse the file being recorded currently
        input_files = input_files[:-1]

        # Check each input file
        for file_name in input_files:
            # If this file hasn't been transcribed yet
            if f'{file_name}.txt' not in output_files:
                # Transcribe the file
                transcription = send_to_api(str(os.path.join(input_directory, file_name)))
                
                if debug:
                    print(f"{thread_number}-{file_name}-{transcription}")

                # Save the transcription to a text file
                with open(os.path.join(output_directory, f'{file_name}.txt'), 'w', encoding='utf-8') as f:
                    f.write(transcription)

                # If the transcription contains the stop word, set the flag
                if 'stop' in transcription.lower():
                    stop_threads = True
                    speak("Stopped")
                    return

def combine_transcriptions(thread_number):
    # Directory for this thread's transcriptions
    directory = f'../data/thread{thread_number}_out'

    # Get the list of text files in the directory
    text_files = sorted([f for f in os.listdir(directory) if f.endswith('.txt')])

    # Initialize an empty string to hold all the transcriptions
    all_transcriptions = ''

    # Read each text file
    for file_name in text_files:
        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as f:
            # Append the transcription to the combined transcription string
            all_transcriptions += f.read() + " "

    # Return the combined transcription
    return all_transcriptions

def prompt_transcriptions(num_threads):
    """Combine transcriptions ready for prompt."""
    prompt = ""
    for i in range(num_threads):
        prompt += f"\n>>>{i+1}\n"
        prompt += combine_transcriptions(i+1)
    return prompt

def speak(text="Done", log=False):
    if debug or log:
        print(f">>>{text}")
    speech.say(text, 'en-US')    
    # Block until speech synthesis has finished
    while speech.is_speaking():
        time.sleep(0.1)


if __name__ == '__main__':
    clear_temp_directories(THREADS)
    speak("Recording")

    recorder_threads = [threading.Thread(
        target=record_audio, 
        args=(i+1, (RECORD_TIME/THREADS)*i)) 
        for i in range(THREADS)
        ]
    transcriber_threads = [threading.Thread(
        target=transcribe_audio, 
        args=(i+1,)) 
        for i in range(THREADS)
        ]
    
    # Start all the threads
    for thread in recorder_threads + transcriber_threads:
        thread.start()
    
    # Wait for all threads to finish
    for thread in recorder_threads + transcriber_threads:
        thread.join()
    
    speak("Harmonizing")
    # specify the file path
    prompt_harmonize_transcripts = Path(
        '..', 
        'prompts', 
        'programflow', 
        'harmonize_transcripts.txt'
        ).read_text(encoding='utf-8')
    prompt_harmonize_transcripts += prompt_transcriptions(THREADS)
    if debug:
        print(">>>>>>prompt_harmonize_transcripts")
        print(prompt_harmonize_transcripts)
        print(">>>>>>")
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt_harmonize_transcripts}
      ]
    )
    raw_commands = completion.choices[0].message.content
    speak(raw_commands)

