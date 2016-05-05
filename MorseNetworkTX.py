from MorseNetwork import *

if __name__ == "__main__":
        physicalTX = threading.Thread(target=p.transmit,name="PHYSICALTX")       
        dataLinkTX = threading.Thread(target=dll.transmit,name="DATALINKTX")
        networkTX = threading.Thread(target=n.transmit,name="NETWORKTX")
        applicationTX = threading.Thread(target=a.transmit,name="APPLICATIONTX")
        
        physicalTX.start()
        dataLinkTX.start()
        networkTX.start()
        applicationTX.start()

        applicationTX.join()
        networkTX.join()
        dataLinkTX.join()
        physicalTX.join()
