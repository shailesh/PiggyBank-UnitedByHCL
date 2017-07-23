__author__ = 'MD'
from blockchain.wallet import Wallet
from blockchain import exchangerates
import urllib
import json
import smtplib
import webbrowser
import datetime
import multiprocessing
import pickle
import os
import uuid
import copy

users = {}

"""
This is the main container of the functions required for both the GUI
and the command line tool.

I think you know enough about Bitcoin to understand what this project does.
"""

#This checks if the stack.txt has any data in it and loads it if it does.
#The stack.txt file contains both the key (username) and pass (password)
#to the wallets created with the program.
def init():
    global users
    if os.path.getsize('stack.txt') > 0:
        file1 = open('stack.txt', 'r')
        users = pickle.load(file1)
        file1.close()

#A getter which returns the dictionary of keys and pass.
def getdict():
    return users

#This prints the keys and pass of the dictionary.
def printu():
    for key, value in users.iteritems():
        print key, value

#This returns the id(s) contained in the dictionary
def userData(id):
    ret = users[id]
    return ret

#This function allows new keys and pass(s) to be added to the text file
def insert(id, key):
    users[id] = key
    file2 = open('stack.txt', 'a')
    pickle.dump(users, file2)
    file2.close()

#Generates a random password using the UUID library for a key.
def passGen():
    passkey = uuid.uuid4()
    return passkey

#Using the blockchain API, this function creates a new wallet and saves it into
#the main wallet account which holds all the wallets. The new wallet is then saved.
def mkWallet():
    password = passGen()
    from blockchain import createwallet
    wallet = createwallet.create_wallet(password, 'cd6938f8-cd49-4aa0-a766-27c4b6d812c4', label='piggybank')
    global users
    users[wallet.identifier] = password
    file2 = open('stack.txt', 'w+')
    pickle.dump(users, file2)
    file2.close()
    return wallet.identifier

#Returns how much Bitcoin a wallet has.
def getBTC(id, key):
    wallet = Wallet(id, key)
    sbtc = 100000000
    bal = float(wallet.get_balance())
    if bal == 0 or bal == '':
        btc = "balance is zero"
    else:
        btc = bal/sbtc
    return btc

#Returns how much Bitcoin a wallet has in USD.
def currentUSD(id, key):
    b = getBTC(id, key)
    if b != "balance is zero":
        ticker = "https://btc-e.com/api/2/btc_usd/ticker"
        data = urllib.urlopen(ticker)
        jdata = json.loads(data.read())
        usdVal = jdata['ticker']['sell']
        ret = usdVal*b
    else:
        ret = "balance is zero"
    return ret

#This function generates a public QR code which can be used to add funds to
#a particular wallet. The QR images are saved in /qr.
def pay(id, key):
    wallet = Wallet(id, key)
    add = wallet.list_addresses()
    newadd = add[0].address
    qr_api = 'https://blockchain.info/qr?data={}&size=200'
    qr_code = qr_api.format(newadd)
    webbrowser.open_new(qr_code)
    return qr_code

#Returns information about an address using the blockchain API.
def addressDetails(address):
    chainAddress = "https://api.chain.com/v2/bitcoin/addresses/%s?api-key-id=931008adbbb3d91045ba1b0b87397e17" % (address)
    request = urllib.urlopen(chainAddress)
    adict = json.loads(request.read())
    return adict

#This function also creates a QR code but is used to display it on the GUI widget.
def getQRaddress(id, key):
    wallet = Wallet(id, key)
    add = wallet.list_addresses()
    newadd = add[0].address
    qr_api = 'https://blockchain.info/qr?data={}&size=200'
    qr_code = qr_api.format(newadd)
    return qr_code

#A helper function to download the QR code using the blockchain API.
def downloadQR(id, key):
    import os
    xpath = "qr\\" + str(id) + '.png'
    if not os.path.isfile(xpath):
        url = getQRaddress(id, key)
        path = urllib.urlretrieve(url, os.path.join('qr', id))
        path = path[0]
        os.rename(path, (path + '.png'))
        path = path + '.png'
        return path
    else:
        return xpath

#This function sends a text message with the key and pass to a TMOBILE
#number using SMTP.
def txt(number, id, key):
    user = 'temppiggy1@gmail.com'
    number = str(number) + '@tmomail.net'
    password = 'piggybank123'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    #sending the id
    server.sendmail(user, number, str(id))
    #sending the key
    server.sendmail(user, number, str(key))
    server.quit()

#This function allows the key and pass to be texted at a certain time.
#For the sake of testing, it sends it 5 seconds after. The better case
#would be to send the pass and key after a year.
def timer(number, id, key):
    now = datetime.datetime.now()
    now = now.second
    nextmin = now + 5
    while True:
        if datetime.datetime.now().second >= nextmin:
            txt(number, id, key)
            break

#A helper function which allows the timer to run in the background since the
#time interval can vary.
def inittimer(number, id, key):
    process = multiprocessing.Process(target=timer, args=[number, id, key])
    process.start()
    now = datetime.datetime.now().minute
    now += 3
    if datetime.datetime.now().minute >= now:
        process.terminate()
    return

#Gets the current exchange rates and stores it in a dictionary which is returned.
def ticker():
    eDict = copy.deepcopy(exchangerates.get_ticker())
    return eDict

#Using bitcoinaverage API, the Bitcoin amount is converted to USD.
def toUSD(btc):
    url = 'https://api.bitcoinaverage.com/ticker/global/USD/last'
    data = (urllib.urlopen(url)).read()
    data = float(btc)*float(data)
    return data

#This function allows a regular email to be send instead of a text message.
#The input is checked on the GUI implementation if the user inputs an
#email or a phone number.
def regemail(number, id, key):
    user = 'piggybankbit@gmail.com'
    password = 'piggybank12345'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    #sending the id
    server.sendmail(user, number, str(id))
    #sending the key
    server.sendmail(user, number, str(key))
    server.quit()
