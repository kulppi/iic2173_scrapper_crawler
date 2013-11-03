import urllib2
from bs4 import BeautifulSoup
from pymongo import MongoClient

def ScrapingRottenTomatoes(scrapercollection, url):
    req = urllib2.Request(url, None, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(BeautifulSoup(html).prettify())
    titleTag = soup.find("span", {"itemprop": "name"})
    if not titleTag:
        titleTag = soup.find("h1", {"class": "movie_title"}).find_all("span")[0]
    titleAux = titleTag.contents[0].strip()
    title = titleAux[:len(titleAux)-7]
    year = titleAux[len(titleAux)-5:len(titleAux)-1]
    cast = soup.find("div", {"id": "cast-info"}).find_all(itemprop="name")
    genres = soup.find("div", {"class": "left_col"}).find_all(itemprop="genre")
    synopsis = soup.find("p",{"id": "movieSynopsis"}).contents[0].strip()
    rating = soup.find("span",{"id": "all-critics-meter"}).contents[0].strip()
    image = soup.find("div", {"class": "media_block_image movie_poster_area"}).find('img')['src']
    generos = []
    for genre in genres:
       generos.append(genre.contents[0].strip())
    actores = []
    for actor in cast:
        actores.append(actor.contents[0].strip())
    movie = {"Title": title, "Year": year, "Rating": rating, "Genres": generos, "Synopsis": synopsis, "Cast": actores, "Site" : 'RottenTomatoes', "Image" : image, "URL" : url}
    scrapercollection.insert(movie)

def mainScraperRotten():
    client = MongoClient()
    db1 = client.crawlerdb
    db2 = client.scraperdb
    crawlercollection = db1.rt
    scrapercollection = db2.scrapercollection
    while True:
        document = crawlercollection.find_one({"readed" : None})
        if document:
            try:
                ScrapingRottenTomatoes(scrapercollection, document["url"])
            except:
                document["invalid"] = True
            document["readed"] = True
            crawlercollection.save(document)

if __name__ == '__main__':
    mainScraperRotten()
