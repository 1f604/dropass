import sys
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import filedialog
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