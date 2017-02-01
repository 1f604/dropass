#Description of functionality:
#1. Checks for config file. If config file not exist or not in right format, create new config file by asking for path of password file and the master password. Goto 2
#If password file not exist or cannot be decrypted with password supplied, again create new config file.
#2. When the user clicks on save button, the contents of the file is encrypted with the master password and then saved at path.

import sys

import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import os.path
from tkinter import filedialog

def createnewconfig():
    global filepath
    global password
    filepath = input("Enter the full path+filename of your new password file (will be created if not already exists): ")
    password = input("Enter your master password: ")

#1. Check if config exists. If not then create new config.
try:
    import dropassconfig
    filepath = dropassconfig.config['filepath']
    password = dropassconfig.config['password']
except:
    print("Could not find a valid config file. Creating new config:")
    createnewconfig()
else:
    print("Settings successfully imported from config file")

#2. If file exists then try to decrypt it, otherwise encrypt some string using the user's master password

if os.path.isfile(filepath):
    contents = decrypt(filepath) #throws exception if this fails
else:
    f = open(filepath, "wb") #encrypt some lines using the password
    for i in range(10):
        f.write("This is line %d\r\n" % (i + 1))
    f.close()
    contents = decrypt(filepath)
















root=tk.Tk("Passwords Editor - DroPass")

frame = tk.Frame(root, bg='brown')
frame.pack(fill='both', expand='yes')
text=tkst.ScrolledText(
    master = frame,
    wrap   = 'word',  # wrap text at full words only
    width  = 80,      # characters
    height = 30,      # text lines
    bg='beige'        # background color of edit area
)
text.grid()
def saveas():
    global text
    t = text.get("1.0", "end-1c")
    savelocation=filedialog.asksaveasfilename()
    file1=open(savelocation, "w+")
    file1.write(t)
    file1.close()
button=tk.Button(root, text="Save", command=saveas)
root.mainloop()