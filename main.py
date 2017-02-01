#Description of functionality:
#1. Checks for config file. If config file not exist or not in right format, create new config file by asking for path of password file and the master password. Goto 2
#If password file not exist or cannot be decrypted with password supplied, again create new config file.
#2. When the user clicks on save button, the contents of the file is encrypted with the master password and then saved at path.

import sys
from cryptotest import encrypt, decrypt
import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import os.path
from tkinter import filedialog
import base64


conf = "dropass.config"










def createnewconfig():
    global filepath
    filepath = input("Enter the full path+filename of your password file (will be created if not already exists): ")
    #password = input("Enter your master password: ")# Yeah, don't do this.
    with open(conf, "w") as f:
        f.write(filepath)  # encrypt some lines using the password

#1. Check if config exists. If not then create new config
if os.path.isfile(conf):
    with open(conf, "r") as f:
        filepath = f.read()
    if os.path.isfile(filepath):
        print("Settings successfully imported from config file")
    else:
        print("Config file not valid. Creating new config.")
        createnewconfig()
else:
    print("Config file not found. Creating new config.")
    createnewconfig()

#2. If file exists then try to decrypt it, otherwise encrypt some string using the user's master password

#    password = dropassconfig.config['password'] #LOL. Don't do this.
if not os.path.isfile(filepath):
    print("File not found. Creating new file.")
    password = input("Enter your new master password: ")
    with open(filepath, "wb") as f:
        f.write(encrypt("Enter your passwords in this file 23123",password))#encrypt some lines using the password
else:
    print("Found existing file.")
    password = input("Enter the master password for the file: ")
with open(filepath,"rb") as f:
    s = f.read()
contents = decrypt(s,password) #throws exception if this fails
print(contents)















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