"""This is the module of GUI"""
import tkinter
from tkinter import filedialog
import tkinter.ttk as ttk
import gui_ops as ops

import Models.gui_component as container

COPYRIGHT_SYMBOL = u"\u00A9"

# get WINDOW object
WINDOW = tkinter.Tk()
# set WINDOW size
WINDOW.geometry('1040x550')
# restrict minimize and maximize
WINDOW.resizable(0, 0)
# add background image
BG_IMG = tkinter.PhotoImage(file="gui_component/0.png")
# set background image
BG_LBL = tkinter.Label(WINDOW, image=BG_IMG)
BG_LBL.place(x=0, y=0, relwidth=1, relheight=1)
# add title to app
WINDOW.title("Note Generator for Lecture Video")

""" 0 --> location of the video
    1 --> location of the transcript
    any --> location to save"""


# control the editing text field directly. Force to edit using only clicking folder icon
# text - location
# dir_type - relevant text field
def add_text(text, dir_type):
    """"This method is used to manage text field by restricting user by direct editing"""
    try:
        if dir_type == 0:
            # add text field editable to change using folder icon
            VIDEO_LOC.config(state="normal")
            VIDEO_LOC.delete(0, tkinter.END)
            VIDEO_LOC.insert(0, text)
            # prevent text field editable to change using folder icon
            VIDEO_LOC.config(state="disable")
            return
        elif dir_type == 1:
            TRANSCRIPT_LOC.config(state="normal")
            TRANSCRIPT_LOC.delete(0, tkinter.END)
            TRANSCRIPT_LOC.insert(0, text)
            TRANSCRIPT_LOC.config(state="disable")
        else:
            SAVE_TO_LOC.config(state="normal")
            SAVE_TO_LOC.delete(0, tkinter.END)
            SAVE_TO_LOC.insert(0, text)
            SAVE_TO_LOC.config(state="disable")
        # if all only all 3 field are field then active the generate button
        if len(VIDEO_LOC.get()) != 0 and len(TRANSCRIPT_LOC.get()) != 0 and len(SAVE_TO_LOC.get()) != 0:
            BTN_GENERATE['state'] = "active"
        else:
            # if any text field in not fill, then deactivate the generate button
            BTN_GENERATE['state'] = "disabled"
    # if any error occur all field set to disable
    except Exception:
        VIDEO_LOC.config(state="disable")
        TRANSCRIPT_LOC.config(state="disable")
        SAVE_TO_LOC.config(state="disable")


# 2 is for default parameter value
def select_file_type(dir_type=2):
    """This method used to select location using folder button"""
    try:
        if dir_type == 0:
            # select video location
            file_path = filedialog.askopenfile(filetypes=(("mp4 files", "*.MP4"), ("all files", "*.*")))
            add_text(file_path.name, dir_type)
        elif dir_type == 1:
            # select transcript location
            file_path = filedialog.askopenfile(filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            add_text(file_path.name, dir_type)
        else:
            # save path
            file_path = filedialog.askdirectory()
            add_text(file_path, dir_type)
    except Exception:
        # if error when close the explore without selecting a path
        pass


# For Video Location
# label video location
VIDEO_LBL = tkinter.Label(WINDOW, text="Video Location", font=("Helvetica", 15, "bold"), bg="silver", fg="black")
VIDEO_LBL.place(x=50, y=100)
# text entry for video location
VIDEO_LOC = tkinter.Entry(WINDOW, width=75)
VIDEO_LOC.place(x=350, y=105)
VIDEO_LOC.config(state="disable")
# button for open file explore
ICON_1 = tkinter.PhotoImage(file="gui_component/icon1.png")
SELECT_VIDEO = tkinter.Button(WINDOW, image=ICON_1, bg="silver", command=lambda: select_file_type(0))
SELECT_VIDEO.place(x=960, y=103)

# For Transcript Location
# label transcript location
TRANSCRIPT_LBL = tkinter.Label(WINDOW, text="Transcript Location", font=("Helvetica", 15, "bold",), bg="silver",
                               fg="black")
TRANSCRIPT_LBL.place(x=50, y=180)
# text entry for transcript location
TRANSCRIPT_LOC = tkinter.Entry(WINDOW, width=75)
TRANSCRIPT_LOC.place(x=350, y=185)
TRANSCRIPT_LOC.config(state="disable")

SELECT_TRANSCRIPT = tkinter.Button(WINDOW, image=ICON_1, bg="silver", command=lambda: select_file_type(1))
SELECT_TRANSCRIPT.place(x=960, y=183)

# For Save Directory Location
# label save location
SAVE_TO_LBL = tkinter.Label(WINDOW, text="Save Note To", font=("Helvetica", 15, "bold",), bg="silver",
                            fg="black")
SAVE_TO_LBL.place(x=50, y=260)

# text entry for save location
SAVE_TO_LOC = tkinter.Entry(WINDOW, width=75)
SAVE_TO_LOC.place(x=350, y=265)
SAVE_TO_LOC.config(state="disable")
SELECT_SAVE_DIRECTORY = tkinter.Button(WINDOW, image=ICON_1, bg="silver", command=select_file_type)
SELECT_SAVE_DIRECTORY.place(x=960, y=263)


# method run after generate note button
def start_generation_task():
    """"run after button click"""
    # method call - gui_ops.py module
    ops.start_generation(VIDEO_LOC.get(), TRANSCRIPT_LOC.get(), SAVE_TO_LOC.get())


# button for start generation of note
BTN_GENERATE = tkinter.Button(WINDOW, text="Generate Note", font=("Helvetica", 15, "bold"), bg="silver", fg="black",
                              command=start_generation_task)
BTN_GENERATE.place(x=450, y=350)
BTN_GENERATE['state'] = "disabled"

# location of the progress bar
PROGRESS = ttk.Progressbar(WINDOW, orient=tkinter.HORIZONTAL, length=500, mode='determinate')
PROGRESS.place(x=270, y=420)
# Project Team Name
OWNERSHIP_LABEL = tkinter.Label(WINDOW, text=COPYRIGHT_SYMBOL + " Team-Aztec", font=("Helvetica", 8, "bold",),
                                bg="silver",
                                fg="black")
OWNERSHIP_LABEL.place(x=450, y=525)
# add WINDOW and progress bar references to globally accessible list
container.component.append(WINDOW)
container.component.append(PROGRESS)
# continuous running WINDOW
WINDOW.mainloop()
