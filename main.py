import whisper
import pyaudio
import wave
from datetime import date
import os.path
import torch

#Get Date and create file in google drive folder
this_month = date.today().month
this_year = date.today().year
months_dict= {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
google_drive_path = "G:/My Drive/Diaries/"+str(this_year)+" Diary/"+months_dict[this_month]+"/"
today = str(date.today())
filename = google_drive_path+today+".wav"

#if file already exists, add part number
if os.path.isfile(filename):
    i=1
    filename = google_drive_path+today+"_part_"+str(i)+".wav"
    while os.path.isfile(filename):
        filename = google_drive_path+today+"_part_"+str(i)+".wav"
        i+=1

#UI Prompt
print("Today is: ", today)
p = pyaudio.PyAudio()  # Create an interface to PortAudio


#Recording settings
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

#Record
frames = []  # Initialize array to store frames
try:
    print('Starting recording...')
    print("Press Ctrl+C to stop recording.")        
    while True:
        data = stream.read(chunk)
        frames.append(data)
except:
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print('Finished recording.')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("File saved as: ", filename)
    print("Transcribing...")
    torch.cuda.init()
    device = "cuda" # if torch.cuda.is_available() else "cpu"
    print("Is cuda available:", torch.cuda.is_available())
    model = whisper.load_model("turbo").to(device)
    diary_text = model.transcribe(filename)
    #write to txt file
    txt_filename = filename.replace(".wav", ".txt")
    with open(txt_filename, "w", encoding="utf-8") as file:
        file.write(diary_text["text"])
    print("˗ˏˋ ★ ˎˊ˗⸜(｡˃ ᵕ ˂ )⸝♡ᯓ★.𖥔 ݁ ˖° ༘ ೀ⋆｡°")
    print("Transcription saved as: ", txt_filename)
    print("Well done writing your diary today! ୧(๑•̀ヮ•́)૭")
    file.close()