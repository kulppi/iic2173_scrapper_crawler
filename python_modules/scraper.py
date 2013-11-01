import scraperRT
import scraperIMDB
import threading

def main():
    t1 = threading.Thread(target=scraperIMDB.mainScraperIMDB)
    t2 = threading.Thread(target=scraperRT.mainScraperRotten)
    t1.start(); t2.start()

if __name__ == '__main__':
    main()
