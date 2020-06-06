from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


import subprocess

def getFile():
    filename = filedialog.askopenfilename()
    try:
        f = open(filename)
    except (FileNotFoundError, TypeError):
        messagebox.showinfo("Open File", "File not choosed")
    else:
        f.close()
        sc = 'xxd -g1 {}'.format(filename)
        s = subprocess.check_output(sc.split())
        text.insert(1.0, s)
        l['bg'] = '#CCCCFF'
        l['text'] = filename.split('/')[-1]

def saveFile():
    file = filedialog.asksaveasfilename(filetypes=(("text files", "*.txt"), ("All files", "*.*")))
    try:
        f = open(file, 'w')
    except (FileNotFoundError, TypeError):
        messagebox.showinfo("Save File", "File not saved...")
    else:
        s = text.get(1.0, END)
        out = subprocess.run(["xxd", "-r", "-g1", "-", file], input=s.encode("UTF-8"), stdout=subprocess.PIPE)
        text.delete(1.0, END)
        f.close()

root = Tk()
root.title='Editor'
root["bg"] = '#FFFFCC'
w = root.winfo_screenwidth() // 2 - 200
h = root.winfo_screenheight() // 2 - 200
root.geometry('+{}+{}'.format(w, h) )

l = Label(bg = '#FFFFCC')
l.grid(row = 0, columnspan=2)

fr = Frame()
fr.grid(row =1, columnspan=2, sticky=N+W+E)
text = Text(fr, bg = '#CCCCCC', fg = '#006600', width=50, height=20, wrap=NONE)
text.pack(side=LEFT)
scroll = Scrollbar(fr, command=text.yview)
scroll.pack(fill=Y, side=LEFT)
text.config(yscrollcommand=scroll.set)

b1 = Button(text="Open", command=getFile, width=8, height=2, fg = "#123FEA")
b1.grid(row=2, sticky=E)
b2 = Button(text="Save", command=saveFile, width=8, height=2, fg = "#123FEA")
b2.grid(row=2, column=1, sticky=W)
root.mainloop()
