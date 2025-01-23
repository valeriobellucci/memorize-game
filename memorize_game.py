#!/usr/bin/env python3

# Path to the folder where the data are located
folder_path = '/Users/damiano/Desktop/German/Nicole' ### CHANGE HERE ###

# Files pattern to load
file_pattern = "Neues*.xlsx"  # Pattern for .xlsx files starting with "Neues"


###################################################
# Game Interface

import tkinter as tk
from tkinter import scrolledtext, font, messagebox
import random
import pandas as pd
import glob
import os

##### Load database and check for new data #####

# Path to the database file
database_name = 'database.xlsx'
working_folder = os.getcwd()
excel_database = os.path.join(working_folder,database_name)

# load or creates the database
if os.path.isfile(excel_database):
    # Read the Excel file into a dictionary of DataFrames, treating NaN as empty strings
    dataframes_dict = pd.read_excel(excel_database, sheet_name=None, na_values=['NaN'],
                                    keep_default_na=False)
else:
    # create new dataframe
    dataframes_dict = {}


# Iterate over all files in the folder matching the pattern
for file_path in glob.glob(os.path.join(folder_path, file_pattern)):
    # Extract filename without extension
    file_name = os.path.basename(file_path).split('.')[0]

    # Check if the file name already exists in the dictionary
    if file_name not in dataframes_dict:

        # Load the Excel file
        excel_file = pd.ExcelFile(file_path)

        # Get the number of sheets in the file
        num_sheets = len(excel_file.sheet_names)

        ### 1st sheet ###
        # Load the 1st sheet of the excel file into a DataFrame (sheet 0)
        df_1 = excel_file.parse(sheet_name=0)

        # Rename the 1st and 2nd column
        df_1.columns = ['German', 'English']

        # Clean the DataFrame and create a copy
        cleaned_df_1 = df_1.dropna(how='all').copy()

        # Add weights column
        cleaned_df_1['weights'] = 1

        # Add notes column
        cleaned_df_1['notes'] = ""

        if num_sheets == 1:
            cleaned_df = cleaned_df_1

        elif num_sheets == 2:
            ### 2nd sheet ###
            # Load the 2nd sheet of the excel file into a DataFrame (sheet 1)
            df_2 = excel_file.parse(sheet_name=1)

            # Assuming the German word is always followed by its English translation and description
            # Create two separate DataFrames for German and English rows
            df_german = df_2.iloc[::2].reset_index(drop=True)  # German words on even rows
            df_english = df_2.iloc[1::2].reset_index(drop=True)  # English translations on odd rows

            # Combine the two DataFrames
            combined_df = pd.concat([df_german, df_english], axis=1)

            # Rename columns
            combined_df.columns = ['German', 'English_Description']

            # Split the English and Description columns
            combined_df[['English', 'notes']] = combined_df['English_Description'].str.split(' - ', expand=True)

            # Now drop the 'English_Description' column
            combined_df.drop(columns=['English_Description'], inplace=True)

            # Clean the DataFrame and create a copy
            cleaned_df_2 = combined_df.dropna(how='all').copy()

            # Add weights column
            cleaned_df_2['weights'] = 1

            # Reorder the columns
            cleaned_df_2 = cleaned_df_2[['German', 'English', 'weights', 'notes']].copy()

            ### Merge the two sheets
            sheets = [cleaned_df_1, cleaned_df_2]
            cleaned_df = pd.concat(sheets)
        
        elif num_sheets == 3:
            ### 3rd sheet ONLY ###
            # Load the 3rd sheet of the excel file into a DataFrame (sheet 2)
            df_3 = excel_file.parse(sheet_name=2)

            # Assuming that the order of rows is always:
            # 1. the German word 
            # 2. its English translation 
            # 3. its description in German
            # Create 3 separate DataFrames
            df_german = df_3.iloc[0::3].reset_index(drop=True)  # German words, on rows starting with 0 and in steps of 3
            df_english = df_3.iloc[1::3].reset_index(drop=True)  # English translations, on rows starting with 1 and in steps of 3
            df_description = df_3.iloc[2::3].reset_index(drop=True)  # Description, on rows starting with 2 and in steps of 3

            # Combine the two DataFrames
            combined_df = pd.concat([df_german, df_english, df_description], axis=1)

            # Rename columns
            combined_df.columns = ['German', 'English', 'notes']

            # Clean the DataFrame and create a copy
            cleaned_df_2 = combined_df.dropna(how='all').copy()

            # Add weights column
            cleaned_df_2['weights'] = 1

            # Reorder the columns
            cleaned_df_2 = cleaned_df_2[['German', 'English', 'weights', 'notes']].copy()

            ### Merge the two sheets
            sheets = [cleaned_df_1, cleaned_df_2]
            cleaned_df = pd.concat(sheets)
        
        else:
            # Display a message box
            print("Unrecognized Data Structure", f"The file '{file_name}'has an unexpected number of sheets.")
 
        
        # reset the index and drop the old index
        cleaned_df.reset_index(drop=True, inplace=True)

        # Store the DataFrame in the dictionary
        dataframes_dict[file_name] = cleaned_df

# Now dataframes_dict contains all the loaded and cleaned DataFrames



##### The Game starts here #####

# global variables
play_click_count = 0
random_row = None
sampled_df = None
random_df = None
play_count = 0
correct_count = 0
false_count = 0
random_row_index = 0


# Function to choose a random sheet
def choose_day():
    global random_df
    random_sheet_name = random.choice(list(dataframes_dict.keys()))
    random_df = dataframes_dict[random_sheet_name]
    sheet_name_display.delete(1.0, tk.END)
    sheet_name_display.insert(tk.INSERT, random_sheet_name, 'center')
    play_click_count = 0
    

# Function to play (choose a random row)
def play():
    global play_click_count, random_row, play_count, random_row_index, sampled_df

    if play_click_count != 0:
        # Save Notes in the current dataframe
        notes_content = notes_display.get("1.0", tk.END)
        random_df.at[random_row_index, "notes"] = notes_content.strip()  # Remove any trailing newlines
        
        # allow to modify the German and English words in the database
        if modify_lock.get():
            german_content = german_display.get("1.0", tk.END)
            random_df.at[random_row_index, "German"] = german_content.strip()  # Remove any trailing newlines
            english_content = english_display.get("1.0", tk.END)
            random_df.at[random_row_index, "English"] = english_content.strip()  # Remove any trailing newlines
    
    # Select a new row only on the first click of each pair
    if play_click_count % 2 == 0:
        
        # Sample one random row and keep it as a DataFrame
        sampled_df = random_df.sample(n=1, weights="weights")

        # Retrieve the index of the sampled row
        random_row_index = sampled_df.index[0]

        # Get the row as a Series
        random_row = sampled_df.iloc[0]
        
        #print("German:", random_row.iloc[0])  # Debugging
        #print("English:", random_row.iloc[1])  # Debugging
        # Increment and display play count
        play_count += 1
        play_count_counter.config(text=f"{play_count}")

    # Update displays based on the toggle state and click count
    if play_click_count % 2 == 0:
        # German and English displays
        german_display.delete(1.0, tk.END)
        english_display.delete(1.0, tk.END)
        if toggle_var.get() == 1:
            german_display.insert(tk.INSERT, sampled_df["German"].iloc[0], 'center')
        else:
            english_display.insert(tk.INSERT, sampled_df["English"].iloc[0], 'center')
        # Scrap display
        scrap_display.delete(1.0, tk.END)
        # Notes display
        notes_display.delete(1.0, tk.END)
        notes_display.insert(tk.INSERT, sampled_df["notes"].iloc[0], 'center')
    else:
        if toggle_var.get() == 1:
            english_display.insert(tk.INSERT, sampled_df["English"].iloc[0], 'center')
        else:
            german_display.insert(tk.INSERT, sampled_df["German"].iloc[0], 'center')

        

    play_click_count += 1


# Function to save the content of notes_display
def save_notes_content():
    global notes_content
    notes_content = notes_display.get("1.0", tk.END)
    
# CORRECT click    
def correct_click():
    global correct_count
    if random_df.at[random_row_index, 'weights'] > 1:
        random_df.at[random_row_index, 'weights'] -= 1 
    correct_count += 1
    correct_count_label.config(text=f"{correct_count}")
    play()

# FALSE click
def false_click():
    global false_count
    random_df.at[random_row_index, 'weights'] += 1
    false_count += 1
    false_count_label.config(text=f"{false_count}")
    play()

# save database
def save():
    with pd.ExcelWriter(excel_database) as writer:
        for key, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=key, index=False)

            
# Setting up the main window
window = tk.Tk()
window.title("Memorize Game")
window.geometry("1200x900")  # Adjust window size as needed (6 times wider)

# Define a larger font
larger_font = font.Font(size=30)


########## row (Choose sheet) ##########

# Initialize row counter
current_row = 0  # Initialize the row counter

# Button to choose a random sheet (day)
choose_day_button = tk.Button(window, text="Choose Day", command=choose_day, font=larger_font)
choose_day_button.grid(row=current_row, column=0)

# Display for the chosen sheet name
sheet_name_display = scrolledtext.ScrolledText(window, height=1, width=60, font=larger_font)
sheet_name_display.tag_configure('center', justify='center')
sheet_name_display.grid(row=current_row, column=1, columnspan=10)


########## row (Play setup) ##########
current_row += 1  # Increment the row counter

# Button to play (choose a random row)
play_button = tk.Button(window, text="Play", command=play, font=larger_font)
play_button.grid(row=current_row, column=0, columnspan=1)

# Shared variable for toggles
toggle_var = tk.IntVar(value=1)  # 1 for German, 2 for English
modify_lock = tk.IntVar(value=0) # 0 non-modifiable, 1 modifiable (for German/English database)

# Checkbuttons as toggles
german_toggle = tk.Checkbutton(window, text="German", variable=toggle_var, onvalue=1, offvalue=2, font=larger_font)
german_toggle.grid(row=current_row, column=1)

english_toggle = tk.Checkbutton(window, text="English", variable=toggle_var, onvalue=2, offvalue=1, font=larger_font)
english_toggle.grid(row=current_row, column=2)

# Button to save (choose a random row)
save_button = tk.Button(window, text="Save", command=save, font=larger_font)
save_button.grid(row=current_row, column=3)

# Allow to modify German/English as toggle
modify_toggle = tk.Checkbutton(window, text="modify German/English", 
                               variable=modify_lock, onvalue=1, offvalue=0, font=larger_font)
modify_toggle.grid(row=current_row, column=4)


########## row (German words) ##########
current_row += 1  # Increment the row counter

# Display for the German word
german_label = tk.Label(window, text="German", font=larger_font)
german_label.grid(row=current_row, column=0)
german_display = scrolledtext.ScrolledText(window, height=2, width=60, font=larger_font)
german_display.config(state="normal")
german_display.tag_configure('center', justify='center')
german_display.grid(row=current_row, column=1, columnspan=10)


########## row (English words) ##########
current_row += 1  # Increment the row counter

# Display for the English translation
english_label = tk.Label(window, text="English", font=larger_font)
english_label.grid(row=current_row, column=0)
english_display = scrolledtext.ScrolledText(window, height=2, width=60, font=larger_font)
english_display.config(state="normal")
english_display.tag_configure('center', justify='center')
english_display.grid(row=current_row, column=1, columnspan=10)


########## row (Scrap box) ##########
current_row += 1  # Increment the row counter

def center_scrap_text(event):
    scrap_display.tag_add("center", "1.0", "end")

# Scrap field for writing
scrap_label = tk.Label(window, text="Scrap", font=larger_font)
scrap_label.grid(row=current_row, column=0)
scrap_display = scrolledtext.ScrolledText(window, height=3, width=60, font=larger_font)
scrap_display.grid(row=current_row, column=1, columnspan=10)
scrap_display.tag_configure('center', justify='center')
scrap_display.bind("<KeyRelease>", center_scrap_text)


########## row (Notes box) ##########
current_row += 1  # Increment the row counter

def center_notes_text(event):
    notes_display.tag_add("center", "1.0", "end")

# Scrap field for writing
notes_label = tk.Label(window, text="Notes", font=larger_font)
notes_label.grid(row=current_row, column=0)
notes_display = scrolledtext.ScrolledText(window, height=3, width=60, font=larger_font)
notes_display.grid(row=current_row, column=1, columnspan=10)
notes_display.tag_configure('center', justify='center')
notes_display.bind("<KeyRelease>", center_notes_text)


########## 3x rows (Correct / False fields) ##########

# Correct button and counter
current_row += 1  # Increment the row counter
correct_button = tk.Button(window, text="Correct", command=correct_click, font=larger_font)
correct_button.grid(row=current_row, column=1)
correct_count_label = tk.Label(window, text="0", font=larger_font, justify='left')
correct_count_label.grid(row=current_row, column=2, sticky='w')

# False button and counter
current_row += 1  # Increment the row counter
false_button = tk.Button(window, text="False", command=false_click, font=larger_font)
false_button.grid(row=current_row, column=1)
false_count_label = tk.Label(window, text="0", font=larger_font)
false_count_label.grid(row=current_row, column=2, sticky='w')

# Play counter
current_row += 1  # Increment the row counter
play_count_label = tk.Label(window, text="Play Count: ", font=larger_font)
play_count_label.grid(row=current_row, column=1)
play_count_counter = tk.Label(window, text="0", font=larger_font)
play_count_counter.grid(row=current_row, column=2, sticky='w')


# Define the on_enter_press function
def on_enter_press(event):
    if not (event.state & 0x0001):  # Check if Shift is not pressed
        play()
        if not (play_click_count % 2 == 0):
            scrap_display.delete(1.0, tk.END)


# Bind the Enter key to the on_enter_press function
window.bind("<Return>", on_enter_press)

# Run the application
window.mainloop()

 


# In[ ]:





# In[ ]:





# In[ ]:




