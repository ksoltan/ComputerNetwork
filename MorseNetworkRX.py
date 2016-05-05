from MorseNetwork import *

if __name__ == "__main__":
        print('Starting')
        physicalRX = threading.Thread(target=p.receive,name="PHYSICALRX")
        dataLinkRX = threading.Thread(target=dll.receive,name="DATALINKRX")
        networkRX = threading.Thread(target=n.receive,name="NETWORKRX")
        applicationRX = threading.Thread(target=a.receive,name="APPLICATIONRX")
        
        physicalRX.start()
        print('Started physical')
        dataLinkRX.start()
        print('Started datalink')
        networkRX.start()
        applicationRX.start()
        
        applicationRX.join()
        networkRX.join()
        dataLinkRX.join()
        physicalRX.join()
        print('Hi, I have ended all processes')
