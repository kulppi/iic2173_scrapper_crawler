from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

def ScrapingIMDB(html, scrapercollection, url):
	error = False
	soup = BeautifulSoup(BeautifulSoup(html).prettify())
	titleTag = soup.find("span", {"class": "title-extra"})
	if not titleTag and soup.find("h1", {"class": "header"}).find_all("span"):
		titleTag = soup.find("h1", {"class": "header"}).find_all("span")[0]
	if titleTag:
		title = titleTag.contents[0].strip().replace('\"','')
	else:
		error = True
	if not error:	
		if soup.find("h1", {"class": "header"}).find("a"):
			year = soup.find("h1", {"class": "header"}).find("a").contents[0].strip()
		else:
			error = True
		if not error:
			if soup.find("table", {"class": "cast_list"}).find_all(itemprop="actor"):
				cast = soup.find("table", {"class": "cast_list"}).find_all(itemprop="actor")
			else:
				error = True
			if not error:
				if soup.find("div", {"class": "infobar"}).find_all(itemprop="genre"):
					genres = soup.find("div", {"class": "infobar"}).find_all(itemprop="genre")
				else:
					error = True
				if not error:
					if soup.find("div",{"id": "titleStoryLine"}).find("div",{"itemprop":"description"}).find("p"):
						synopsis = soup.find("div",{"id": "titleStoryLine"}).find("div",{"itemprop":"description"}).find("p").contents[0].strip()
					else:
						error = True
					if not error:
						if soup.find("div",{"class": "star-box-giga-star"}):
							rating = soup.find("div",{"class": "star-box-giga-star"}).contents[0].strip()
						else:
							error = True
						if not error:
							if soup.find("div", {"class": "image"}):
								image = soup.find("div", {"class": "image"})['src']
							else:
								error = True
							if not error:
								generos = []
								for genre in genres:
									generos.append(genre.contents[0].strip())
								actores = []
								for actor in cast:
									actores.append(actor.a.span.contents[0].strip())
								movie = {"Title": title, "Year": year, "Rating": rating, "Genres": generos, "Synopsis": synopsis, "Cast": actores, "Site" : 'IMDB', "Image" : image, "URL" : url}
								scrapercollection.insert(movie)
	if error:
		return False
	else:
		return True

def ScrapingRottenTomatoes(html, scrapercollection):
	soup = BeautifulSoup(BeautifulSoup(html).prettify())
	titleTag = soup.find("span", {"itemprop": "name"})
	if not titleTag:
	    titleTag = soup.find("h1", {"class": "movie_title"}).find_all("span")[0]
	titleAux = titleTag.contents[0].strip()
	title = titleAux[:len(titleAux)-7]
	year = titleAux[len(titleAux)-5:len(titleAux)-1]
	cast = soup.find("div", {"id": "cast-info"}).find_all(itemprop="name")
	genres = soup.find("body").find_all(itemprop="genre")
	synopsis = soup.find("p",{"id": "movieSynopsis"})
	rating = soup.find("span",{"id": "all-critics-meter"})
	if not rating:
		rating = "No rating"
	else:
		rating = rating.contents[0].strip()
	generos = []
	for genre in genres:
	   generos.append(genre.contents[0].strip())
	actores = []
	for actor in cast:
	    actores.append(actor.contents[0].strip())
	movie = {"Title": title, "Year": year, "Rating RottenTomatoes": rating, "Genres": generos, "Synopsis RottenTomatoes": synopsis.contents[0].strip(), "Cast": actores, "Site" : 1}
	scrapercollection.insert(movie)

def main():
	client = MongoClient()
	db = client.crawlerdb
	#crawlercollection = db.crawlercollection
	crawlercollection = db.mycollection
	scrapercollection = db.scrapercollection
	while True:
		document = crawlercollection.find_one({"read" : None})
		if document:
			try:
				if not "showtimes" in document["url"] and not "reviews" in document["url"]:
					if "imdb" in document["url"]:
						ScrapingIMDB(document["html"], scrapercollection, document["url"])
					elif "rottentomatoes" in document["url"]:
						ScrapingRottenTomatoes(document["html"], scrapercollection)	
			except:
				document["invalid"] = True
			document["read"] = True
			crawlercollection.save(document)
		else:
			time.sleep(10)


if __name__ == '__main__':
	main()
