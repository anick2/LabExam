from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import subprocess


fl = 0
in1, in2 = 0, 0
colored = True

def getFile():
    global filename
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

def saveFile(event, save_type):
    if (save_type == 'saveas'):
        file = filedialog.asksaveasfilename(filetypes=(("text files", "*.txt"), ("All files", "*.*")))
    else:
        file = filename
    try:
        f = open(file, 'w')
    except (FileNotFoundError, TypeError):
        messagebox.showinfo("Save File", "File not saved...")
    else:
        s = text.get(1.0, END)
        out = subprocess.run(["xxd", "-r", "-g1", "-", file], input=s.encode("UTF-8"), stdout=subprocess.PIPE)
        f.close()

def findSym(event):
    global fl, in1, in2
    textk = ek.get()
    text.tag_config("here", background="yellow", foreground="blue")
    s = text.get(1.0, END)
    index = str.find(s, textk, fl + 1)
    lab['bg'] = 'pink'
    lab["text"] = str(str.count(s, textk)) + " matches found"
    if index == -1:
        messagebox.showinfo("Attention", "Not found")
        fl = 0
    else:
        if in1 != 0 and in2 != 0:
            text.tag_remove("here", in1, in2)
        fl = index
        in1 = str(index // 76 + 1) + "." + str(index % 76)
        in2 = str((index + len(textk)) // 76 + 1) + "." + str((index + len(textk)) % 76)
        text.tag_add("here", in1, in2)

def change():
    textt = et.get()
    s = text.get(1.0, "end")
    text.delete(1.0, END)
    text.insert(1.0, s.replace(ek.get(), textt))


def changeSym():
    global fl, in1, in2, et
    win = Toplevel()
    win.title('Change')
    et = Entry(win)
    et.grid(columnspan = 2)
    bt1 = Button(win, text = "Change", command=change)
    bt1.grid(column=0, row=1)
    bt2 = Button(win, text="Exit", command=win.destroy)
    bt2.grid(column=1, row=1)
    win.mainloop()

def findText():
    global ek, fl, lab, in1, in2
    fl = 0
    in1, in2 = 0, 0
    win = Toplevel(bg = 'grey', width = 100, height = 19)
    win.resizable(False, False)
    win.title('Find')
    ek = Entry(win)
    ek.grid(row = 0, columnspan = 3, padx = 3, pady = 3)
    lab = Label(win, bg = 'grey', height = 3)
    lab.grid(row=1, columnspan = 3)
    bk1 = Button(win, text = "Find", width = 5, height = 2)
    bk2 = Button(win, text = "Close", command = win.destroy, width = 5, height = 2)
    bk1.grid(row = 2, column = 0, sticky = N)
    bk1.bind('<Button-1>', findSym)
    bk2.grid(row = 2, column = 2, sticky = N)
    bk3 = Button(win, text="Change", command=changeSym, width = 5, height = 2)
    bk3.grid(row=2, column=1, sticky=N)
    win.mainloop()

def deleteText():
    text.delete(1.0, END)
    l['bg'] = '#FFFFCC'
    l['text'] = ''

def colorText():
    global colored
    colored = not colored
    text.tag_config("address", foreground="red")
    text.tag_config("value", foreground="blue")
    text.tag_config("comment", foreground="black")
    s = text.get(1.0, END)
    n = len(s) // 76
    if len(s) % 76: n += 1
    if colored == False:
        for i in range(1,n + 1):
            text.tag_add("address", str(i) + '.0', str(i) + '.9')
            text.tag_add("value", str(i) + '.10', str(i) + '.58')
            text.tag_add("comment", str(i) + '.59', str(i) + '.end')
    else:
        for i in range(1,n + 1):
            text.tag_remove("address", str(i) + '.0', str(i) + '.9')
            text.tag_remove("value", str(i) + '.10', str(i) + '.58')
            text.tag_remove("comment", str(i) + '.59', str(i) + '.end')

root = Tk()
root.title('Editor')
root.resizable(False, False)
root["bg"] = '#FFFFCC'
w = root.winfo_screenwidth() // 2 - 200
h = root.winfo_screenheight() // 2 - 200
root.geometry('+{}+{}'.format(w, h) )

l = Label(bg = '#FFFFCC')
l.grid(row = 0, columnspan=6)
ek = Entry()
fr = Frame()
fr.grid(row =1, columnspan=6, sticky=N+W+E)
text = Text(fr, bg = '#CCCCCC', fg = '#006600', wrap=NONE)
text.pack(side=LEFT)
scroll = Scrollbar(fr, command=text.yview)
scroll.pack(fill=Y, side=LEFT)
text.config(yscrollcommand=scroll.set)

b1 = Button(text="Open", command=getFile, width=8, height=2, fg = "#123FEA")
b1.grid(row=2, column = 0, sticky=S)
b2 = Button(text="Save", width=8, height=2, fg = "#123FEA")
b2.grid(row=2, column = 4, sticky=S)
b3 = Button(text="Find", command=findText, width=8, height=2, fg = "#123FEA")
b3.grid(row=2, column = 2, sticky=S)
b4 = Button(text="Clear", command=deleteText, width=8, height=2, fg = "#123FEA")
b4.grid(row=2, column = 3, sticky=S)
b5 = Button(text="Color", command=colorText, width=8, height=2, fg = "#123FEA")
b5.grid(row=2, column = 1, sticky=S)
b6 = Button(text="Save As", width=8, height=2, fg = "#123FEA")
b6.grid(row=2, column = 5, sticky=S)
b6.bind('<Button-1>', lambda event, f="saveas": saveFile(event, f))
b2.bind('<Button-1>', lambda event, f="save": saveFile(event, f))

root.mainloop()
