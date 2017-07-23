__author__ = 'Shailesh'
import piggybank
'''
This allows you to use most of the functions that are
available in the GUI on a command line interface.
'''
if __name__ == '__main__':
    piggybank.init()
    piggybank.printu()
    id = raw_input("id: ")
    number = raw_input("tmo number: ")
    key = piggybank.userData(id)
    while True:
        print "pay | btc | txt | make | print | exit"
        inputx = raw_input(">>> ")
        if inputx == 'pay':
            piggybank.pay(id, key)
        elif inputx == 'print':
            piggybank.printu()
        elif inputx == 'make':
            id = piggybank.mkWallet()
            key = piggybank.userData(id)
        elif inputx == 'btc':
            print piggybank.getBTC(id, key)
        elif inputx == 'usd':
            print piggybank.currentUSD(id, key)
        elif inputx == 'txt':
            piggybank.inittimer('piggybankbit', 'piggybank12345', number, id, key)
        elif inputx == 'exit':
            break
        else:
            print " wrong input"
