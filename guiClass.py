__author__ = 'Shailesh'
from Tkinter import *
import piggybank
import tkMessageBox
from PIL.ImageTk import PhotoImage

#This function formats the keys and passes in a more prettier format
#so it is more understandable in the GUI.
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

#This is the right frame which holds the blob of keys and passes.
#A text widget and scrollbar is used.
class frame2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=0, column=1)
        self.widgets()

    def widgets(self):
        self.accounts = Text(self, wrap=WORD)
        val = formatDict(dict)
        self.accounts.insert(INSERT, val)
        self.accounts.config(state=DISABLED)
        self.accounts.grid(row=0, column=0)
        self.scrollbar = Scrollbar(self, command=self.accounts.yview)
        self.scrollbar.grid(row=0, column=0, sticky='nsew')
        self.accounts['yscrollcommand'] = self.scrollbar.set

#This is the main frame, the left frame. This allows you to manage many of
#the wallets' functionality. There are a bunch of labels, entry, button,
#listbox, and scrollbar widgets used.
class frame1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.widgets()

    def widgets(self):
        self.label1 = Label(self, text="KEY:")
        self.label2 = Label(self, text="PASS:")
        self.label3 = Label(self, text="NUM:")
        self.id0 = Entry(self, width=40)
        self.key0 = Entry(self, width=40)
        self.number0 = Entry(self, width=40)
        self.label1.grid(row=0, sticky=W)
        self.id0.grid(row=0, column=1, columnspan=2)
        self.label2.grid(row=1, sticky=W)
        self.key0.grid(row=1, column=1, columnspan=2)
        self.label3.grid(row=2, sticky=W)
        self.number0.grid(row=2, column=1, columnspan=2)

        self.scrollbar2 = Scrollbar(self)
        self.scrollbar2.grid(row=7, column=0, sticky=N+S+E)
        self.label4 = Label(self, text="List of keys:")
        self.lb = Listbox(self, width=40, yscrollcommand=self.scrollbar2.set)
        self.label4.grid(row=7, sticky=W)
        self.updatelb()
        self.lb.bind('<<ListboxSelect>>', self.sel)
        self.scrollbar2.config(command=self.lb.yview)

        self.b1 = Button(self, text='btc', command=self.btc, width=10)
        self.b2 = Button(self, text='usd', command=self.usd, width=10)
        self.b3 = Button(self, text='text', command=self.text, width=10)
        self.b4 = Button(self, text='make', command=self.make, width=10)
        self.b5 = Button(self, text='QR', command=self.pay, width=10)
        self.b6 = Button(self, text='reset', command=self.clear, width=46)
        self.b1.grid(row=4, column=0)
        self.b2.grid(row=4, column=1)
        self.b3.grid(row=5, column=0)
        self.b4.grid(row=5, column=1)
        self.b5.grid(row=6, column=0)
        self.b6.grid(row=3, columnspan=2)
#This function updates the listbox when a new wallet is created.
    def updatelb(self):
        for key in dict.keys():
            self.lb.insert(END, key)
        self.lb.grid(row=7, column=1, columnspan=2)
#Function for the reset button.
    def clear(self):
        self.id0.delete(0, END)
        self.key0.delete(0, END)
        self.number0.delete(0, END)
#Allows the selected key/pass combo to be automatically added to the entry widgets.
    def sel(self, e):
        selected = self.lb.curselection()
        self.clear()
        print id
        self.id0.insert(END, self.lb.get(selected))
        self.key0.insert(END, dict[self.lb.get(selected)])
#Runs the getBTC function.
    def btc(self):
        id = self.id0.get()
        key = self.key0.get()
        try:
            ret = piggybank.getBTC(id, key)
            tkMessageBox.showinfo('btc', ret)
        except:
            tkMessageBox.showinfo('error', 'verify KEY and PASS')
#Runs the getUSD function.
    def usd(self):
        id = self.id0.get()
        key = self.key0.get()
        try:
            ret = piggybank.currentUSD(id, key)
            tkMessageBox.showinfo('usd', ret)
        except:
            tkMessageBox.showinfo('error', 'verify KEY and PASS')
#Handles whether the you input a email or a number and depending on that
#it will apply the right function to execute a email or text.
    def text(self):
        id = self.id0.get()
        key = self.key0.get()
        number = self.number0.get()
        try:
            if number != '':
                if not number.isalpha():
                    piggybank.inittimer(number, id, key)
                    tkMessageBox.showinfo('btc', 'sending text...')
                else:
                    piggybank.regemail(number, id, key)
                    tkMessageBox.showinfo('email', 'sending email...')
            else:
                tkMessageBox.showinfo('error', 'check NUM. T-Mobile numbers only.')
        except:
            tkMessageBox.showinfo('error', 'verify KEY, PASS, and NUM')
#This function allows the make wallet button to work.
    def make(self):
        frame2.accounts.config(state=NORMAL)
        piggybank.mkWallet()
        newDict = piggybank.getdict()
        frame2.accounts.delete("1.0", END)
        val = formatDict(dict)
        frame2.accounts.insert(INSERT, val)
        frame2.accounts.grid(row=0, column=0)
        frame2.accounts.config(state=DISABLED)
        tkMessageBox.showinfo('new wallet', 'new wallet created. check list.')
#This generates the QR code on screen.
    def pay(self):
        id = self.id0.get()
        key = self.key0.get()
        try:
            location = piggybank.downloadQR(id, key)
            photo = PhotoImage(file=location)
            label = Label(self, image=photo)
            label.image = photo
            label.grid(row=8, column=1)
        except:
            tkMessageBox.showinfo('error', 'verify KEY and PASS')

#The menubar widget contains some basic tools and information.
#I think it is self explanatory.
class Menubar(Menu):
    def __init__(self, master):
        Menu.__init__(self, master)

        tools = Menu(self, tearoff=False)
        self.add_cascade(label="Tools", underline=0, menu=tools)
        tools.add_command(label="Exchange Rates", underline=1, command=self.exchange)
        tools.add_separator()
        tools.add_command(label="Address Data", underline=1, command=self.addData)

        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Options", underline=0, menu=fileMenu)
        fileMenu.add_command(label="About", underline=1, command=self.about)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)

    def about(self):
        text = '''
        Title: Bitcoin Piggy Bank
        Author: MD Islam
        Version: 1.0

        This program uses Blockchain's API
        to manage Bitcoin wallets.

        The idea behind this utility is to allow
        people to learn about Bitcoin. Users
        are only allowed to get their public key.
        The public key only allows for Bitcoin
        to be added to the individual's wallet.

        The utility is for the backend to deploy
        wallets quickly and manage them easily.
        The idea was pitched to me by the founder
        of Chain.com during NYU's Leslie eLab's first
        hackathon. I also coded much of it
        during the hackathon.
        '''
        tkMessageBox.showinfo('About', text)

    def exDict(self):
        eDict = piggybank.ticker()
        val = '''Unit\tValue\n'''
        for k, v in eDict.iteritems():
            val += "%s\t" % k
            val += "%s\n" % v.p15min
        val += "\n*Rates within 15 minutes."
        return val

    def eRefresh(self):
        self.flow.config(state=NORMAL)
        val = self.exDict()
        self.flow.delete(1.0, END)
        self.flow.insert(INSERT, val)
        self.flow.config(state=DISABLED)

    def exchange(self):
        val = self.exDict()
        self.container2 = Toplevel()
        self.container2.iconbitmap('favicon.ico')
        self.container2.resizable(width=FALSE, height=FALSE)
        self.flow = Text(self.container2, width=25)
        self.flow.insert(INSERT, val)
        self.flow.config(state=DISABLED, background="black", foreground="green")
        self.flow.grid(row=1, column=0)
        self.refresh = Button(self.container2, text='refresh', command=self.eRefresh, width=15)
        self.refresh.grid(row=0, column=0)

    def addData(self):
        self.container3 = Toplevel()
        obj = addDetails(self.container3)
        self.container3.resizable(width=FALSE, height=FALSE)
        self.container3.iconbitmap('favicon.ico')

#This is a helper class which allows for the address data to be displayed
#in a comprehensible way using blockchain API.
class addDetails(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.widget()

    def widget(self):
        self.entry = Entry(self, width=60)
        self.entry.grid(row=0, column=0, sticky=W)
        self.enter = Button(self, text="Enter", command=self.load)
        self.infobox = Text(self, width=45, height=10)
        self.infobox.config(state=DISABLED, background="black", foreground="green")
        self.infobox.grid(row=1, column=0)
        self.enter.grid(row=0, column=0, sticky=E)

    def dataFormat(self):
        data = piggybank.addressDetails(self.entry.get())
        address = data[0]['address']
        balance = data[0]['total']['balance']
        received = data[0]['total']['received']
        sent = data[0]['total']['sent']
        #confirmed data:
        cbalance = data[0]['confirmed']['balance']
        creceived = data[0]['confirmed']['received']
        balance = piggybank.toUSD(balance/100000000)
        received = piggybank.toUSD(received/100000000)
        sent = piggybank.toUSD(sent/100000000)
        cbalance = piggybank.toUSD(cbalance/100000000)
        creceived = piggybank.toUSD(creceived/100000000)
        text = 'Address: {0}\nBalance: {1}\nReceived: {2}\nSent: {3}\n\nConfirmed:\nBalance: {4}\nReceived: {5}\n\n*Values in USD'.format(address, balance, received, sent, cbalance, creceived)
        return text
#This checks if the input address is valid or not.
    def load(self):
        try:
            data = self.dataFormat()
            self.infobox.config(state=NORMAL)
            self.infobox.delete(1.0, END)
            self.infobox.insert(INSERT, data)
            self.infobox.config(state=DISABLED)
        except KeyError:
            tkMessageBox.showinfo("error", "Unable to locate address.")

#This initializes the Tk GUI.
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        menubar = Menubar(self)
        self.config(menu=menubar)
        self.title('pig terminal')
        self.iconbitmap('favicon.ico')
        self.resizable(width=FALSE, height=FALSE)

if __name__ == '__main__':
    piggybank.init()
    dict = piggybank.getdict() #This generates the dictionary of keys and passes.

    App = App()
    frame2 = frame2(App)
    frame1 = frame1(App)
    App.mainloop()
