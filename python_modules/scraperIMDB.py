#import requests
from urllib import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient

def ScrapingIMDB(scrapercollection, url):
    #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #print url
    html = urlopen(url).read()
    #print 'ok'
    soup = BeautifulSoup(BeautifulSoup(html).prettify())
    #print 'okImport'
    #if not soup.find("div", {"id": "titleTVSeries"}) and not soup.find("div", {"id": "titleTVEpisodes"}):
    titleTag = soup.find("span", {"class": "title-extra"})
    if not titleTag:
        titleTag = soup.find("h1", {"class": "header"}).find_all("span")[0]
    title = titleTag.contents[0].strip().replace('\"','')
    year = soup.find("h1", {"class": "header"}).find("a").contents[0].strip()
    cast = soup.find("table", {"class": "cast_list"}).find_all(itemprop="actor")
    genres = soup.find("div", {"class": "infobar"}).find_all(itemprop="genre")
    synopsis = soup.find("div",{"id": "titleStoryLine"}).find("div",{"itemprop":"description"}).find("p").contents[0].strip()
    rating = soup.find("div",{"class": "star-box-giga-star"}).contents[0].strip()
    image = soup.find("div", {"class": "image"}).find('img')['src']
    generos = []
    for genre in genres:
        generos.append(genre.contents[0].strip())
    actores = []
    for actor in cast:
        actores.append(actor.a.span.contents[0].strip())
    movie = {"Title": title, "Year": year, "Rating": rating, "Genres": generos, "Synopsis": synopsis, "Cast": actores, "Site" : 'IMDB', "Image" : image, "URL" : url}
    scrapercollection.insert(movie)
    #print 'listo'
    #print 'nolisto'

def mainScraperIMDB():
    client = MongoClient()
    db1 = client.crawlerdb
    db2 = client.scraperdb
    crawlercollection = db1.imdb
    scrapercollection = db2.scrapercollection
    while True:
        document = crawlercollection.find_one({"readed" : None})
        if document:
            try:
                ScrapingIMDB(scrapercollection, document["url"])
            except:
                document["invalid"] = True
            document["readed"] = True
            crawlercollection.save(document)

if __name__ == '__main__':
    mainScraperIMDB()
