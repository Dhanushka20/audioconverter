import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
from pydub import AudioSegment
import pyttsx3
import os

# Function to read and display the text from the selected file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf8") as file:
                text = file.read()
                text_display.delete(1.0, tk.END)
                text_display.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

# Function to read aloud the displayed text
def read_text():
    text = text_display.get(1.0, tk.END).strip()
    if text:
        lang = language_var.get()
        if lang == 'si':
            tts = gTTS(text=text, lang=lang)
            tts.save("temp.mp3")
            os.system("start temp.mp3")  # Use 'start' on Windows, 'open' on macOS, 'xdg-open' on Linux
        elif lang == 'en':
            speaker = pyttsx3.init()
            voices = speaker.getProperty('voices')
            # Select the male English voice
            for voice in voices:
                if 'en' in voice.languages and 'male' in voice.name.lower():
                    speaker.setProperty('voice', voice.id)
                    break
            # Adjust the speech rate if needed
            rate = speaker.getProperty('rate')
            speaker.setProperty('rate', rate - 25)
            speaker.say(text)
            speaker.runAndWait()
    else:
        messagebox.showinfo("Info", "No text to read.")

# Function to save the audio in MP3 format
def save_as_mp3():
    text = text_display.get(1.0, tk.END).strip()
    if text:
        lang = language_var.get()
        if lang == 'si':
            tts = gTTS(text=text, lang=lang)
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if file_path:
                tts.save(file_path)
                messagebox.showinfo("Success", "Audio saved successfully.")
        elif lang == 'en':
            speaker = pyttsx3.init()
            voices = speaker.getProperty('voices')
            for voice in voices:
                if 'en' in voice.languages and 'male' in voice.name.lower():
                    speaker.setProperty('voice', voice.id)
                    break
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if file_path:
                speaker.save_to_file(text, file_path)
                speaker.runAndWait()
                messagebox.showinfo("Success", "Audio saved successfully.")
    else:
        messagebox.showinfo("Info", "No text to save.")

# Function to save the audio in WAV format
def save_as_wav():
    text = text_display.get(1.0, tk.END).strip()
    if text:
        lang = language_var.get()
        if lang == 'si':
            tts = gTTS(text=text, lang=lang)
            tts.save("temp.mp3")
            audio = AudioSegment.from_mp3("temp.mp3")
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if file_path:
                audio.export(file_path, format="wav")
                messagebox.showinfo("Success", "Audio saved successfully.")
            os.remove("temp.mp3")
        elif lang == 'en':
            speaker = pyttsx3.init()
            voices = speaker.getProperty('voices')
            for voice in voices:
                if 'en' in voice.languages and 'male' in voice.name.lower():
                    speaker.setProperty('voice', voice.id)
                    break
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if file_path:
                speaker.save_to_file(text, "temp.wav")
                speaker.runAndWait()
                audio = AudioSegment.from_wav("temp.wav")
                audio.export(file_path, format="wav")
                os.remove("temp.wav")
                messagebox.showinfo("Success", "Audio saved successfully.")
    else:
        messagebox.showinfo("Info", "No text to save.")

# Create the main window
root = tk.Tk()
root.title("Text-to-Speech with Tkinter")
root.geometry("600x400")

# Create and place the widgets
btn_open = tk.Button(root, text="Open Text File", command=open_file)
btn_open.pack(pady=10)

btn_read = tk.Button(root, text="Read Aloud", command=read_text)
btn_read.pack(pady=10)

btn_save_mp3 = tk.Button(root, text="Save as MP3", command=save_as_mp3)
btn_save_mp3.pack(pady=10)

btn_save_wav = tk.Button(root, text="Save as WAV", command=save_as_wav)
btn_save_wav.pack(pady=10)

text_display = tk.Text(root, wrap=tk.WORD)
text_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Dropdown menu for language selection
languages = [("Sinhala", "si"), ("English", "en")]
language_var = tk.StringVar(value="en")

language_menu = tk.OptionMenu(root, language_var, *["Sinhala", "English"])
language_menu.pack(pady=10)

# Run the main loop
root.mainloop()
