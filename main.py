
###
### FILE: main.py (ENTRY POINT)
### PROJECT: winf-file-browsie
### AUTHOR: CHARLES EDWARD DOWLING JUNIOR
###

###
### IMPORTS
###

import shlex, subprocess
import os
import tkinter as tk
from tkinter import *
from tkinter import Tk

###
### GLOBAL VARIABLES INIT
###

#Directory of program I.E. Main.py - Does not change
program_dir = os.getcwd()

#Directory of current working directory - changes during the operation of program
current_dir = os.getcwd()

#Placeholder that is utilized during program operation. Keeps track of file opened in file editor.
opened_file = ""

###
### WINDOW CREATION
###

window = Tk()

#Create left side

console_label = tk.Label(window,text="CONSOLE WINDOW")
console_label.grid(column=0,row=0,sticky="NSEW")

console_window = tk.Text(window)
console_window.grid(column=0,row=1,sticky="NSEW")
console_window.configure(state=DISABLED)

#entry_frame = tk.Frame(window)
#entry_frame.grid(column=0,row=2)

console_entry_label = Label(window,text="Command Entry:")
console_entry_label.grid(column=0,row=2)

console_entry = Entry(window)
console_entry.grid(column=0,row=3,columnspan=2,sticky="NSEW")


#Create Text Editor

editor_label = tk.Label(window, text="FILE EDITOR: NO CURRENTLY OPENED FILE")
editor_label.grid(column=1,row=0)

editor_window = tk.Text(window)
editor_window.grid(column=1,row=1,sticky="NSEW")

#Automatic Resizing

Grid.rowconfigure(window,0,weight=0)
Grid.rowconfigure(window,1,weight=1)
Grid.rowconfigure(window,2,weight=0)
Grid.columnconfigure(window,0,weight=1)
Grid.columnconfigure(window,1,weight=1)





def entry_enter_pressed(a=0):

    #Bring the global variables in so I can use and/or modify them
    global current_dir
    global program_dir
    global opened_file

    #This shit-biscuit of a line because it'll throw an error if it doesn't exist.
    outcome = ""

    #Enable the console window to be updatable
    console_window.configure(state="normal")

    ### Work around to ensure that the "cd command works properly"
    ### Also allows for a shifting CWD
    if (console_entry.get()[0:2] == "cd"):
        if (console_entry.get()[3:5] == ".."):

            # Find the last occurence of the \ in the file string
            higher_directory_folder = current_dir.rfind("\\")

            #Sets the current working directory to the next folder up
            current_dir = current_dir[0:int(higher_directory_folder)]

            #Clear the entry box
            console_entry.delete(0,"end")

            #Shell output since actual shell outputs nothing
            outcome = "\nChanged CWD to: " + current_dir + "\n\n"

        elif (console_entry.get()[4:5] == ":"):
            command_str = console_entry.get()
            if (os.path.exists(console_entry.get()[3:len(command_str)]) == True):

                if (console_entry.get()[5:6] == "\\"):
                    
                    current_dir = console_entry.get()[3:len(command_str)]

                    #Clear the entry box, data no longer needed
                    console_entry.delete(0,"end")
                    
                    outcome = "\nChanged CWD to: " + current_dir + "\n"

                else:
                    current_dir = console_entry.get()[3:len(command_str)] + "\\"

                    #Clear the entry box, data no longer needed
                    console_entry.delete(0,"end")

                    outcome = "\nChanged CWD to: " + current_dir + "\n"

            else:
                outcome = "\nRequested location " + console_entry.get()[3:len(command_str)] + " does not exist!\n"

                #Clear the entry box, data no longer needed
                console_entry.delete(0,"end")

        else:

            #Refactor the command so that the shell runs it properly
            command = shlex.split(console_entry.get())

            #Necessary to get the length for index end
            command_str = console_entry.get()

            #Run the command in the shell
            outcome = subprocess.check_output(command, cwd=current_dir, shell=True, text=True)

            #Change the current working directory to something that works (Code below will not run if previous line of code does not work.)
            current_dir = current_dir + "\\" + console_entry.get()[3:len(command_str)]

            #Clear the entry box, data no longer needed
            console_entry.delete(0,"end")

            #Shell output since actual shell outputs nothing
            outcome = "\nChanged CWD to: " + current_dir + "\n\n"

    #Clear Screen Command
    elif (console_entry.get()[0:3] == "cls" or console_entry.get()[0:5] == "clear"):
        console_window.delete("1.0","end")
        #Clear the entry box, data no longer needed
        console_entry.delete(0,"end")

    #Help command prints available commands
    elif (console_entry.get()[0:4] == "help"):
        
        #Open up custom help file because help command does not work with subprocess
        with open(program_dir + "\\help.info", "r") as help:
            for line in help:
                 console_window.insert("end", line)

        #Prettify 100%%%%%%
        console_window.insert("end", "\n")

        #Clear the entry box, data no longer needed
        console_entry.delete(0,"end")

    #Opens a requested file in CWD
    elif (console_entry.get()[0:4] == "open"):

        command_str = console_entry.get()
        try:
            with open((os.path.abspath( current_dir + "\\" + console_entry.get()[5:len(command_str)])), "r") as file:
                for line in file:
                    editor_window.insert("end", line)

            opened_file = current_dir + "\\" + console_entry.get()[5:len(command_str)]

            editor_label.configure(text=("FILE EDITOR: " + opened_file))

            outcome = "\nOpened file \"" + console_entry.get()[5:len(command_str)] + "\" in editor!\n"
        except:
            outcome = "No file specified!"

        #Clear the entry box, data no longer needed
        console_entry.delete(0,"end")

    #Creates file in CWD
    elif (console_entry.get()[0:6] == "create"):

        command_str = console_entry.get()
        open(console_entry.get()[7:len(command_str)], "x")

        outcome = "\nCreated file \"" + console_entry.get()[7:len(command_str)] + "\" in " + current_dir + "!\n"

        #Clear the entry box, data no longer needed
        console_entry.delete(0,"end")
    
    #Saves file in CWD
    elif (console_entry.get()[0:4] == "save"):
        command_str = console_entry.get()
        if (len(command_str) == 4):
            if (opened_file == "" ):

                #Clear the entry box, data no longer needed
                console_entry.delete(0,"end")

                outcome = "ERROR: No currently opened file"

            else:
                with open(os.path.abspath(opened_file), "w") as file:
                    file.write(editor_window.get(1.0,END))

                #Clear the entry box, data no longer needed
                console_entry.delete(0,"end")

                outcome = "\nSaved data to file: " + opened_file + "\n"

        else:
            with open((os.path.abspath( current_dir + "\\" + console_entry.get()[5:len(command_str)])), "w") as file:
                file.write(editor_window.get(1.0,END))

            outcome = "\nSaved data to file: " + command_str[6:len(command_str)] + "\n"

            #Clear the entry box, data no longer needed
            console_entry.delete(0,"end")


    elif (console_entry.get()[0:3] == "del"):

        command = shlex.split(console_entry.get())
        command_str = console_entry.get()

        if (os.path.exists(command_str[4:len(command_str)]) == True):
            subprocess.check_output(command, cwd=current_dir, shell=True, text=True)
            outcome = "\nFile \"" + command_str[4:len(command_str)] + "\" deleted\n"
        else:
            outcome = "\nFILE NOT FOUND!\n"

    else:

        #Format the command with flags and whatnot
        command = shlex.split(console_entry.get())

        #Run the command and generate console output -> outcome
        outcome = subprocess.check_output(command, cwd=current_dir, shell=True, text=True)

        #Clear the entry box, data no longer needed
        console_entry.delete(0,"end")

    #Update Console Window
    console_window.insert("end",outcome)
    console_window.configure(state=DISABLED)

    #Scroll to bottom of window where code is outputted.
    console_window.see(tk.END)

def window_opened(a=0):
    #Selects command entry bar as focused
    console_entry.focus()

    #Initilizes Console window
    console_window.configure(state=NORMAL)
    console_window.insert("1.0", subprocess.check_output("dir", cwd=current_dir, shell=True, text=True))
    console_window.configure(state=DISABLED)

    window.unbind("<Visibility>")

###
### BINDS
###

#Send command whenever the user presses enter
console_entry.bind("<Return>", entry_enter_pressed)
window.bind("<Visibility>", window_opened)

#START APPLICATION
window.mainloop()