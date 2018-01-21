#Description of functionality:
#1. Checks for config file. If config file not exist or not in right format, create new config file by asking for path of password file and the master password. Goto 2
#If password file not exist or cannot be decrypted with password supplied, again create new config file.
#2. When the user clicks on save button, the contents of the file is encrypted with the master password and then saved at path.
 
from cryptotest import encrypt, decrypt
import tkinter as tk
from tkinter import messagebox 
import tkinter.scrolledtext as tkst
import os.path
import getpass  
import os

conf = "dropass.config"
teal='#008080'
brown='#800000'
grey='#808080'
filepath = ""
curSavedFileContents = ""

# This is the list of all default command in the "Text" tag that modify the text
commandsToRemove = (
"<Control-Key-h>",
"<Meta-Key-Delete>",
"<Meta-Key-BackSpace>",
"<Meta-Key-d>",
"<Meta-Key-b>",
"<<Redo>>",
"<<Undo>>",
"<Control-Key-t>",
"<Control-Key-o>",
"<Control-Key-k>",
"<Control-Key-d>",
"<Key-Insert>",
"<<PasteSelection>>",
"<<Clear>>",
"<<Paste>>",
"<<Cut>>",
"<Key-BackSpace>",
"<Key-Delete>",
"<Key-Return>",
"<Control-Key-i>",
"<Key-Tab>",
"<Shift-Key-Tab>"
)

allowed_keys = set({'Up', 'Down', 'Left', 'Right', '<Ctrl-C>'})



def createnewconfig():
    global filepath
    filepath = input("Enter the full path+filename of your password file (will be created if not already exists, leave empty to create default file in data dir): ")
    if filepath == "":
        filepath = "data/passwords.encrypted"
    with open(conf, "w") as f:
        f.write(filepath)  # encrypt some lines using the password

def getTextboxContents():
    global text
    return text.get("1.0", "end-1c")

def saveas(event=None):
    global dirty
    global curSavedFileContents
    plaintext = getTextboxContents()
    curSavedFileContents = plaintext
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
    plaintext = getTextboxContents()
    if plaintext != curSavedFileContents:
        frame.configure(bg=brown)
        dirty = True        
    else:
        frame.configure(bg=teal)
        dirty = False
    text.edit_modified(0)  # IMPORTANT - or <<Modified>> will not be called later.

#def on_focus_out(event):
#    if event.widget == root:
#        frame.configure(bg=grey)
#
#def on_focus_in(event):
#    if event.widget == root:
#        if dirty:
#            frame.configure(bg=brown)            
#        else:
#            frame.configure(bg=teal)

# Select all the text in textbox
def select_all(event):
    wid = event.widget
    wid.tag_add(tk.SEL, "1.0", tk.END)
    return 'break'
# Select current line in textbox
def select_line(event): 
    wid = event.widget
    tk.current_line = wid.index(tk.INSERT)
    wid.tag_add(tk.SEL, "insert linestart", "insert lineend+1c")
    return 'break'
    #after(interval, self._highlight_current_line)

def askpassword():
    password1 = getpass.getpass("Enter your new master password: ")
    password2 = getpass.getpass("Enter your new master password again: ")
    if (password1 != password2):
        print("Passwords do not match, file not created, try again.") #don't create the file if the passwords don't match
        exit(1)
    if not password1:
        print("YOU MUST ENTER A PASSWORD! File not created, try again.")
        exit(1)
    return password1

def createnewfile(password):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(encrypt("Enter your passwords in this file.",password)) #encrypt some lines using the password

def do_nothing(event):
    return "break"
    
def move_cursor(event):
    if event.keysym in allowed_keys:
        return
    else:
        return "break"

def copy(widget, event):
    widget.clipboard_clear()
    txt = widget.get("sel.first", "sel.last")
    widget.clipboard_append(txt)

def custom_paste(event):
    try:
        event.widget.delete("sel.first", "sel.last")
    except:
        pass
    event.widget.insert("insert", event.widget.clipboard_get())
    return "break"

if __name__ == "__main__":
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

    if not os.path.isfile(filepath):
        print("File not found. Creating new file.")
        password = askpassword()
        createnewfile(password)
    else:
        print("Found existing file.")
        password = getpass.getpass("Enter the master password for the file: ")
    with open(filepath,"rb") as f:
        s = f.read()
    contents = decrypt(s,password) #throws exception if this fails
    curSavedFileContents = contents

    #3. Main window setup
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
    text.grid(row=0, column=0)
    newtext=tkst.ScrolledText(
        master = frame,
        wrap   = 'word',  # wrap text at full words only
        width  = 80,      # characters
        height = 5,      # text lines
        bg='beige',        # background color of edit area
        undo=True
    )
    newtext.grid(row=1, column=0)
    text.bind('<<Modified>>', ismodified)
#    text.bind("<FocusIn>", on_focus_in)
#    text.bind("<FocusOut>", on_focus_out)
    button=tk.Button(root, text="Save", command=saveas,   padx=8, pady=8)
    button.pack()
    # the padx/pady space will form a frame
    #text.pack(fill='both', expand=True, padx=8, pady=8)
#    text.grid(padx=8, pady=(8,0))
#    newtext.grid(padx=8, pady=8)
    
    for key in commandsToRemove:
        text.bind(key, do_nothing)
    text.bind("<Key>", move_cursor)
        

    text.insert('insert', contents)
    #text.configure(state="disabled") #makes text read-only
    text.bind("<1>", lambda event: text.focus_set()) #allow text to be copyable
    dirty = False
    frame.configure(bg=teal)

    root.bind_all("<Control-w>", checkUnsavedChanges)
    root.bind_all("<Control-s>", saveas)
    text.bind("<Control-a>", select_all)
    text.bind("<Control-d>", select_line)
    text.bind("<Control-c>", copy)
    newtext.bind("<Control-a>", select_all)
    newtext.bind("<Control-d>", select_line)
    newtext.bind("<Control-c>", copy) 
    newtext.bind("<<Paste>>", custom_paste)

    root.protocol('WM_DELETE_WINDOW', checkUnsavedChanges)  # root is your root window

    #4. main loop
    root.mainloop()
