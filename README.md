# memorize-game
Custom game for practicing vocabulary words collected during language lessons. 
It has a GUI and repeats more often the words more difficult to memorize.
The program was made for practicing German vocabulary, but it can be adapted to any language.

INSTRUCTIONS
1. Save the vocabulary in .xlsx with name starting with "Neues", as in the example .xlsx file. You can save the vocabulary in 3 different formats, visible in the 3 sheets:
    1st sheet: 1st column German words, 2nd column English words. This is useful for the words saved in the Notizen of Preply
    2nd sheet: alternated German and English words
    3rd sheet: 3 alternated rows: German word, English word, German explanation

2. Open memorize_game.py with an IDE or txt editor. Change the folder_path to the path to the folder where you are storing the .xlsx files. Save the file.

3. Launch the memorize_game.py file, via an IDE or:
    In Windows: click on the file or select Open with > Choose another app > Python
    In Mac: right-click on the folder > Services > Open terminal at folder
    

## Detailed explanation ## 
Here's how you can set it up on both Mac and Windows:

For Windows:
Install Python: Make sure Python is installed on your system. You can download it from the official Python website. During installation, ensure that you check the option to "Add Python X.X to PATH" to make Python accessible from the command line.
Associate .py files with Python:
Right-click on your .py file, select Open with > Choose another app.
Select Python from the list, or browse to the Python executable (python.exe) if it's not listed. This is typically found in the Scripts folder inside your Python installation directory.
Make sure to check the option "Always use this app to open .py files" before you click OK.
After this setup, you should be able to double-click a .py file to run it.

For macOS:
Install Python: Python 2.7 is pre-installed on macOS, but it's recommended to use Python 3. You can install Python 3 via Homebrew (a package manager for macOS) by running brew install python in the Terminal, or by downloading it from the Python website.
Make your script executable and add a shebang line:
Open the Terminal and navigate to the directory containing your .py file.
Add a "shebang" line at the top of your .py file. This line tells your system to use Python to interpret the script. It should look something like this: #!/usr/bin/env python3.
Make your .py file executable by running chmod +x program.py in the Terminal.
Create an Automator Application (Optional for easier access):
Open Automator (found in the Applications folder).
Choose to create a new Application.
Drag and drop the Run Shell Script action into the workflow.
In the text field that appears, enter python3 /path/to/your/script.py, replacing /path/to/your/script.py with the actual path to your Python script.
Save the Automator Application wherever you like. You can now run your Python script by double-clicking this application.
These steps should allow you to run a Python script by double-clicking on it in both Windows and macOS environments. However, keep in mind that if your script requires console input or you want to see output printed by the script, it's better to run it from a command line or Terminal to ensure you see the output and can interact with it as needed.
