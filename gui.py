__author__ = 'Shailesh'
from Tkinter import *
import piggybank
import tkMessageBox
from PIL.ImageTk import PhotoImage


#piggybank.insert('33d99a82-2463-458f-96b5-20fbf0ec36dc', 'piggybank123456789')


def btc():
    id = id0.get()
    key = key0.get()
    try:
        ret = piggybank.getBTC(id, key)
        tkMessageBox.showinfo('btc', ret)
    except:
        tkMessageBox.showinfo('error', 'verify KEY and PASS')


def usd():
    id = id0.get()
    key = key0.get()
    try:
        ret = piggybank.currentUSD(id, key)
        tkMessageBox.showinfo('usd', ret)
    except:
        tkMessageBox.showinfo('error', 'verify KEY and PASS')


def text():
    id = id0.get()
    key = key0.get()
    number = number0.get()
    try:
        piggybank.inittimer('piggybankbit', 'piggybank12345', number, id, key)
        tkMessageBox.showinfo('btc', 'sending text...')
    except:
        tkMessageBox.showinfo('error', 'verify KEY, PASS, and NUM')

def formatDict(dict):
    val = '''key:\t\t\t\t\tpassword:\n'''
    number = 1
    for k, v in dict.items():
        output = ''
        output += str(number) + ": "
        number += 1
        output += str(k)
        output += ": " + str(v)
        val += output + "\n"
    return val


def make():
    accounts.config(state=NORMAL)
    piggybank.mkWallet()
    tkMessageBox.showinfo('new bank', 'new piggy bank created!')
    newDict = piggybank.getdict()
    accounts.delete("1.0", END)
    val = formatDict(dict)
    accounts.insert(INSERT, val)
    accounts.grid(row=0, column=0)
    accounts.config(state=DISABLED)


def updatelb():
    for key in dict.keys():
        lb.insert(END, key)
    lb.grid(row=7, column=1, columnspan=2)


def sel(e):
    selected = lb.curselection()
    clear()
    print id
    id0.insert(END, lb.get(selected))
    key0.insert(END, dict[lb.get(selected)])


def pay():
    id = id0.get()
    key = key0.get()
    try:
        location = piggybank.downloadQR(id, key)
        photo = PhotoImage(file=location)
        label = Label(leftframe, image=photo)
        label.image = photo
        label.grid(row=8, column=1)
    except:
        tkMessageBox.showinfo('error', 'verify KEY and PASS')


def clear():
    id0.delete(0, END)
    key0.delete(0, END)
    number0.delete(0, END)

if __name__ == '__main__':
    #id = '33d99a82-2463-458f-96b5-20fbf0ec36dc'
    #key = 'piggybank123456789'

    piggybank.init()
    dict = piggybank.getdict()
    container = Tk()
    container.resizable(width=FALSE, height=FALSE)

    leftframe = Frame(container)
    rightframe = Frame(container)
    container.title("pig terminal")
    container.iconbitmap('favicon.ico')

    accounts = Text(rightframe, wrap=WORD)
    val = formatDict(dict)
    accounts.insert(INSERT, val)
    accounts.config(state=DISABLED)
    accounts.grid(row=0, column=0)
    scrollbar = Scrollbar(rightframe, command=accounts.yview)
    scrollbar.grid(row=0, column=0, sticky='nsew')
    accounts['yscrollcommand'] = scrollbar.set

    label1 = Label(leftframe, text="KEY:")
    label2 = Label(leftframe, text="PASS:")
    label3 = Label(leftframe, text="NUM:")
    id0 = Entry(leftframe, width=40)
    key0 = Entry(leftframe, width=40)
    number0 = Entry(leftframe, width=40)
    label1.grid(row=0, sticky=W)
    id0.grid(row=0, column=1, columnspan=2)
    label2.grid(row=1, sticky=W)
    key0.grid(row=1, column=1, columnspan=2)
    label3.grid(row=2, sticky=W)
    number0.grid(row=2, column=1, columnspan=2)

    scrollbar2 = Scrollbar(leftframe)
    scrollbar2.grid(row=7, column=0, sticky=N+S+E)
    label4 = Label(leftframe, text="List of keys:")
    lb = Listbox(leftframe, width=40, yscrollcommand=scrollbar2.set)
    label4.grid(row=7, sticky=W)
    updatelb()
    lb.bind('<<ListboxSelect>>', sel)
    scrollbar2.config(command=lb.yview)

    b1 = Button(leftframe, text='btc', command=btc, width=10)
    b2 = Button(leftframe, text='usd', command=usd, width=10)
    b3 = Button(leftframe, text='text', command=text, width=10)
    b4 = Button(leftframe, text='make', command=make, width=10)
    b5 = Button(leftframe, text='QR', command=pay, width=10)
    b6 = Button(leftframe, text='reset', command=clear, width=46)
    b1.grid(row=4, column=0)
    b2.grid(row=4, column=1)
    b3.grid(row=5, column=0)
    b4.grid(row=5, column=1)
    b5.grid(row=6, column=0)
    b6.grid(row=3, columnspan=2)

    leftframe.grid(row=0, column=0)
    rightframe.grid(row=0, column=1)

    container.mainloop()

