# File-Browsie
Simple File Manager (Command Line) and File Editor written in python.

## Description
File-Browsie is a simple file explorer and file editor for focusing on programming/writing that is very not resource intensive. (The current build only utilizes 13.3MB when loaded and empty. Notepad takes up 29.2MB when loaded and empty)

Contains limited command prompt command functionality. Commands not present in the help command may have limited/non-functionality.

# Build
File-Browsie is built using pyinstaller.
It can be installed by running the pip command through Command Prompt (cmd.exe):

> pip install pyinstaller

After installing pyinstaller you can build it by using Command Prompt to navigate to the directory for the file system you're building for and running the compilation file

> cd windows
> 
> compile.bat

When compiled from source, the exe file will be present under the newly created directory "dist\main".

Run the exe called main.exe to launch the program.
