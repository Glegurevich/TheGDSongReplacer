import os
import shutil
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime

# Ensure ispathselected and ismusicfileselected are global variables
ispathselected = False
ismusicfileselected = False
is_process_button_created = False

def pathselector():
    global ispathselected  # Declare ispathselected as global to modify it
    user_home = os.path.expanduser('~')
    initial_dir = os.path.join('C:', 'Program Files (x86)', 'Geometry Dash', 'Resources')
    global path
    path = filedialog.askdirectory(initialdir=initial_dir)  # Use filedialog.askdirectory() to select a folder
    
    if path:  # Check if a path was selected
        selected_path.set(f'Selected Path: {path}')  # Update the StringVar with the new path
        ispathselected = True
        create_new_button()  # Create 'Select Music File' button

def create_new_button():
    global ismusicfileselected_button
    if ispathselected:
        ismusicfileselected_button = Button(mn, text='Select Music File', command=selectmusicfile)  # Create new button
        ismusicfileselected_button.pack()

def selectmusicfile():
    global ismusicfileselected  # Declare ismusicfileselected as global to modify it
    global music_path
    music_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])  # Open file dialog for MP3 files
       
    if music_path:  # Check if a file was selected
        selected_music_path.set(f'Selected Music File: {music_path}')  # Update the StringVar with the music file path
        ismusicfileselected = True
        check_both_selected()  # Check if both selections are made

def check_both_selected():
    global is_process_button_created
    if ispathselected and ismusicfileselected and not is_process_button_created:
        create_entry_widget()

def create_entry_widget():
    global is_process_button_created, song_id_entry
    entry_label = Label(mn, text='Enter Song ID to Replace:', background='light green')
    entry_label.pack()
    
    # Create an entry widget that only accepts numbers
    vcmd = (mn.register(validate_song_id), '%P')
    song_id_entry = Entry(mn, validate='key', validatecommand=vcmd)
    song_id_entry.pack()

def validate_song_id(new_value):
    if new_value.isdigit() or new_value == "":  # Allow any number of digits or an empty string
        if len(new_value) <= 10:  # Limit to 10 digits
            create_start_process_button()
        else:
            return False
        return True
    else:
        return False

def create_start_process_button():
    global is_process_button_created
    if not is_process_button_created:
        start_process_button = Button(mn, text='Start Process', command=start_process)
        start_process_button.pack()
        is_process_button_created = True

def start_process():
    try:
        song_id = song_id_entry.get()
        music_file_path = selected_music_path.get().split(': ')[1]  # Get the selected music file path
        selected_directory = selected_path.get().split(': ')[1]  # Get the selected directory path

        # Construct the new file path in the GeometryDash directory
        new_file_path = os.path.join(selected_directory, f'{song_id}.mp3')

        # Check if the file already exists in GeometryDash and replace if necessary
        if os.path.exists(new_file_path):
            os.remove(new_file_path)  # Remove existing file
        
        shutil.copy2(music_file_path, new_file_path)  # Copy the music file to GeometryDash with the new name

        messagebox.showinfo("Success", f"Music file transferred and renamed to '{song_id}.mp3' in 'GeometryDash' directory.")
        
        # Log the process
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file_path = os.path.join(selected_directory, f'log_{current_time}.txt')
        with open(log_file_path, 'w') as file:
            file.write(f'Selected directory: {selected_directory}\n')
            file.write(f'Selected music: {music_file_path}\n')
            file.write(f'Song ID to replace: {song_id}\n')
            file.write('Successfully replaced song with the selected song.\n')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

mn = Tk()
mn.title("Song Replacer for GD")
mn.minsize(800, 600)
mn.configure(background='light green')

selected_path = StringVar()  # Create a StringVar to hold the directory path
selected_path.set('Selected Path:')  # Initialize it with default text

selected_music_path = StringVar()  # Create a StringVar to hold the music file path
selected_music_path.set('Selected Music File:')  # Initialize it with default text

name = Label(mn, text='Song Replacer', background='light green', font=('Script', 48, 'bold'))
name.pack()

filepathlabel = Label(mn, textvariable=selected_path, background='light green')  # Use textvariable to bind to StringVar
filepathlabel.pack()

button1 = Button(mn, text='Select Path', command=pathselector)  # Ensure button is packed to 'mn'
button1.pack()

musicpathlabel = Label(mn, textvariable=selected_music_path, background='light green')  # Use textvariable to bind to StringVar for music path
musicpathlabel.pack()

warninglabel = Label(mn, text='WARNING: If you replace a song, you can\'t get it back, BUT you can do that manually.', background='light green', font=('Impact', 16))
warninglabel.pack()

uselabel = Label(mn, text='You need to enable Change custom songs location first', background='light green', font=('Arial', 16))
uselabel.pack()

text_label = Label(mn, text="©2024/06 Gleb Gurev", padx=10, pady=10, background='light green')
text_label.pack(side=BOTTOM, anchor=W)


mn.iconbitmap('icon.ico')
icon = PhotoImage(file='icon.png')
mn.iconphoto(True,icon)

mn.mainloop()



