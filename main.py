#Description of functionality:
#1. Checks for config file. If config file not exist or not in right format, create new config file by asking for path of password file and the master password. Goto 2
#If password file not exist or cannot be decrypted with password supplied, again create new config file.
#2. When the user clicks on save button, the contents of the file is encrypted with the master password and then saved at path.

import sys
from cryptotest import encrypt, decrypt
import tkinter as tk
from tkinter import * 
import tkinter.scrolledtext as tkst
import os.path
import getpass 
import base64

conf = "dropass.config"
teal='#008080'
brown='#800000'


def createnewconfig():
    global filepath
    filepath = input("Enter the full path+filename of your password file (will be created if not already exists): ")
    #password = input("Enter your master password: ")# Yeah, don't do this.
    with open(conf, "w") as f:
        f.write(filepath)  # encrypt some lines using the password

def saveas(event=None):
    global text
    global dirty
    plaintext = text.get("1.0", "end-1c")
    with open(filepath, "wb") as f:
        f.write(encrypt(plaintext, password))  # encrypt some lines using the password
    dirty = False
    frame.configure(bg=teal)


def checkUnsavedChanges(event=None):
    # check if saving
    # if not:
    if dirty:
        if messagebox.askyesno("Exit", "THERE ARE UNSAVED CHANGES! Do you want to quit the application?"):
            if messagebox.askokcancel("Exit", "THERE ARE UNSAVED CHANGES!! ARE YOU SURE you want to quit the application?"):
                win = tk.Toplevel()
                win.title('warning')
                message = "This will delete stuff"
                tk.Label(win, text=message).pack()
                tk.Button(win, text='No!', command=win.destroy).pack()
                tk.Button(win, text='Delete', command=root.destroy).pack()
                tk.Button(win, text='Noo!', command=win.destroy).pack()
                tk.Button(win, text='Don\'t delete!!', command=win.destroy).pack()
    else:
        root.destroy()

def ismodified(event):
        global dirty
        frame.configure(bg=brown)
        dirty = True
        text.edit_modified(0)  # IMPORTANT - or <<Modified>> will not be called later.

# Select all the text in textbox
def select_all(event):
    text.tag_add(SEL, "1.0", END)
    return 'break'
# Select current line in textbox
def select_line(event): 
    current_line = text.index(INSERT)
    text.tag_add(SEL, "insert linestart", "insert lineend+1c")
    return 'break'
    #after(interval, self._highlight_current_line)

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
        f.write(encrypt("Enter your passwords in this file.",password))#encrypt some lines using the password
else:
    print("Found existing file.")
    password = getpass.getpass("Enter the master password for the file: ")
with open(filepath,"rb") as f:
    s = f.read()
contents = decrypt(s,password) #throws exception if this fails


root=tk.Tk()
root.wm_title("DroPass")
frame = tk.Frame(root, bg=teal)
frame.pack(fill='both', expand='yes')
text=tkst.ScrolledText(
    master = frame,
    wrap   = 'word',  # wrap text at full words only
    width  = 80,      # characters
    height = 30,      # text lines
    bg='beige',        # background color of edit area
    undo=True
)
text.grid()
text.bind('<<Modified>>', ismodified)
button=tk.Button(root, text="Save", command=saveas,   padx=8, pady=8)
button.pack()
# the padx/pady space will form a frame
text.pack(fill='both', expand=True, padx=8, pady=8)

text.insert('insert', contents)
dirty = False
frame.configure(bg=teal)

root.bind_all("<Control-q>", checkUnsavedChanges)
root.bind_all("<Control-s>", saveas)
text.bind("<Control-a>", select_all)
text.bind("<Control-l>", select_line)


root.protocol('WM_DELETE_WINDOW', checkUnsavedChanges)  # root is your root window

root.mainloop()