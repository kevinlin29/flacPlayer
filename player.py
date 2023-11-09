import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pygame import mixer
import os
import random
from mutagen.flac import FLAC

# Initialize Pygame Mixer with the default sampling rate
mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

# Define global variables
playlist = []
current_song_index = -1

# Function to add all FLAC files from the selected directory to the playlist
def add_from_directory():
    directory = filedialog.askdirectory()
    if directory:
        for file in os.listdir(directory):
            if file.endswith(".flac"):
                filepath = os.path.join(directory, file)
                playlist.append(filepath)
                # Get the bit rate for the file using mutagen
                audio = FLAC(filepath)
                bit_rate = int(audio.info.bitrate / 1000)  # Convert to kbps
                # Add file and bit rate to the Listbox
                playlist_box.insert(tk.END, f"{file} - {bit_rate} kbps")
        if len(playlist) > 0:
            play_song(0)

# Functions for the playback control
def play_song(index):
    global current_song_index
    if 0 <= index < len(playlist):
        current_song_index = index
        mixer.music.load(playlist[index])
        mixer.music.play()
        update_playlist_selection()

def play_selected_song(event):
    selected_index = playlist_box.curselection()
    if selected_index:
        play_song(selected_index[0])

def prev_song():
    global current_song_index
    if current_song_index > 0:
        play_song(current_song_index - 1)

def next_song():
    global current_song_index
    if current_song_index < len(playlist) - 1:
        play_song(current_song_index + 1)

def stop_song():
    mixer.music.stop()

def shuffle_play():
    global playlist
    if playlist:
        random.shuffle(playlist)
        update_playlist_box()
        play_song(0)

# Update the Listbox with the shuffled playlist
def update_playlist_box():
    playlist_box.delete(0, tk.END)
    for track in playlist:
        playlist_box.insert(tk.END, os.path.basename(track))

# Update the selection in the Listbox
def update_playlist_selection():
    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_song_index)
    playlist_box.see(current_song_index)
    playlist_box.activate(current_song_index)

def init_mixer(sampling_rate):
    mixer.quit()
    mixer.init(frequency=sampling_rate, size=-16, channels=2, buffer=4096)

# Main GUI setup
root = tk.Tk()
root.title("FLAC Player")
root.geometry('800x600') # Set a larger size for the window

# Styling
style = ttk.Style(root)
style.theme_use('clam')  # You can experiment with 'aqua', 'clam', 'alt', 'default', or 'classic'

# Sampling rate option
sampling_rate_var = tk.IntVar(value=44100)
sampling_rate_label = ttk.Label(root, text="Sampling Rate (Hz):")
sampling_rate_label.pack(side=tk.TOP, pady=5)
sampling_rate_option = ttk.Combobox(root, textvariable=sampling_rate_var, values=[44100, 96000, 192000], state='readonly')
sampling_rate_option.pack(side=tk.TOP, pady=5)
sampling_rate_option.bind("<<ComboboxSelected>>", lambda event: init_mixer(sampling_rate_var.get()))

# Playlist box styling
playlist_frame = tk.Frame(root)
playlist_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
playlist_scrollbar = ttk.Scrollbar(playlist_frame)
playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE, yscrollcommand=playlist_scrollbar.set, relief=tk.FLAT, bg='#f2f2f2')
playlist_box.pack(fill=tk.BOTH, expand=True)
playlist_scrollbar.config(command=playlist_box.yview)

# Playback control buttons
controls_frame = tk.Frame(root)
controls_frame.pack(fill=tk.X, pady=10)

prev_button = ttk.Button(controls_frame, text="Previous", command=prev_song)
prev_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(controls_frame, text="Stop", command=stop_song)
stop_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(controls_frame, text="Next", command=next_song)
next_button.pack(side=tk.LEFT, padx=10)

add_dir_button = ttk.Button(controls_frame, text="Add Directory", command=add_from_directory)
add_dir_button.pack(side=tk.RIGHT, padx=10)

# Playlist box with a binding to play selected song on double-click
playlist_box.bind('<Double-1>', play_selected_song)

# Shuffle play button
shuffle_button = ttk.Button(controls_frame, text="Shuffle Play", command=shuffle_play)
shuffle_button.pack(side=tk.RIGHT, padx=10)

# Run the application
root.mainloop()
