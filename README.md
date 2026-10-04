# keylogger

<h3>EHAX - Project Keylogger</h3>  

This is a local keyboard keylogger that monitors and stores logs designed for input diagnostics and typing analysis.  

Implemented Features:  
-The records are types into <i>keystrokes.log</i>, storing it with timestamps.    
-Special keys with raw scan codes are translated into readable text.  
-Displays the top 5 most pressed keys along with backspace error rate.  
-To end the session - `<CTRL>+<ALT>+<J>`  

The program listens for individual keyboard events, processes each key press, handles special keys, stores them locally.

Example Output:  
<img width="150" height="200" alt="image" src="https://github.com/user-attachments/assets/6778c489-a9c0-496c-815b-67311065ed9a" />

Note: This program does not store hotkeys, as I could not find a solution for it other than hardcoding all of it. Although it does store them individually.
