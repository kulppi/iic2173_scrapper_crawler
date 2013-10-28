import bs4
from pymongo import MongoClient
import time

def ScrapingIMDB(html, scrapercollection, url):
	status = "Success"
	soup = bs4.BeautifulSoup(bs4.BeautifulSoup(html).prettify(), 'lxml')
	if not soup.find("div", {"id": "titleTVSeries"}) and not soup.find("div", {"id": "titleTVEpisodes"}):
		titleTag = soup.find("span", {"class": "title-extra"})
		if not titleTag and soup.find("h1", {"class": "header"}).find_all("span"):
			titleTag = soup.find("h1", {"class": "header"}).find_all("span")[0]
		if titleTag:
			title = titleTag.contents[0].strip().replace('\"','')
		else:
			status = "Fail"
		if status == "Success":	
			if soup.find("h1", {"class": "header"}).find("a"):
				year = soup.find("h1", {"class": "header"}).find("a").contents[0].strip()
			else:
				status = "Fail"
			if status == "Success":
				if soup.find("table", {"class": "cast_list"}).find_all(itemprop="actor"):
					cast = soup.find("table", {"class": "cast_list"}).find_all(itemprop="actor")
				else:
					status = "Fail"
				if status == "Success":
					if soup.find("div", {"class": "infobar"}).find_all(itemprop="genre"):
						genres = soup.find("div", {"class": "infobar"}).find_all(itemprop="genre")
					else:
						status = "Fail"
					if status == "Success":
						if soup.find("div",{"id": "titleStoryLine"}).find("div",{"itemprop":"description"}).find("p"):
							synopsis = soup.find("div",{"id": "titleStoryLine"}).find("div",{"itemprop":"description"}).find("p").contents[0].strip()
						else:
							status = "Fail"
						if status == "Success":
							if soup.find("div",{"class": "star-box-giga-star"}):
								rating = soup.find("div",{"class": "star-box-giga-star"}).contents[0].strip()
							else:
								status = "Fail"
							if status == "Success":
								if soup.find("div", {"class": "image"}):
									image = soup.find("div", {"class": "image"}).find('img')['src']
								else:
									status = "Fail"
								if status == "Success":
									generos = []
									for genre in genres:
										generos.append(genre.contents[0].strip())
									actores = []
									for actor in cast:
										actores.append(actor.a.span.contents[0].strip())
									movie = {"Title": title, "Year": year, "Rating": rating, "Genres": generos, "Synopsis": synopsis, "Cast": actores, "Site" : 'IMDB', "Image" : image, "URL" : url}
									scrapercollection.insert(movie)
	else:
		status = "Serie"	
		return status

def ScrapingRottenTomatoes(html, scrapercollection, url):
	status = "Success"
	soup = bs4.BeautifulSoup(bs4.BeautifulSoup(html).prettify(), 'lxml')
	titleTag = soup.find("span", {"itemprop": "name"})
	if not titleTag and soup.find("h1", {"class": "movie_title"}).find_all("span"):
	    titleTag = soup.find("h1", {"class": "movie_title"}).find_all("span")[0]
	if titleTag:
		titleAux = titleTag.contents[0].strip()
		title = titleAux[:len(titleAux)-7]
		year = titleAux[len(titleAux)-5:len(titleAux)-1]
	else:
		status = "Fail"
	if status == "Success":
		if soup.find("div", {"id": "cast-info"}).find_all(itemprop="name"):
			cast = soup.find("div", {"id": "cast-info"}).find_all(itemprop="name")
		else:
			status = "Fail"
		if status == "Success":
			if soup.find("div", {"class": "left_col"}).find_all(itemprop="genre"):
				genres = soup.find("div", {"class": "left_col"}).find_all(itemprop="genre")
			else:
				status = "Fail"
			if status == "Success":
				if soup.find("p",{"id": "movieSynopsis"}):
					synopsis = soup.find("p",{"id": "movieSynopsis"}).contents[0].strip()
				else:
					status = "Fail"
				if status == "Success":
					if soup.find("span",{"id": "all-critics-meter"}):
						rating = soup.find("span",{"id": "all-critics-meter"}).contents[0].strip()
					else:
						status = "Fail"
					if status == "Success":
						if soup.find("div", {"class": "media_block_image movie_poster_area"}):
							image = soup.find("div", {"class": "media_block_image movie_poster_area"}).find('img')['src']
						else:
							status = "Fail"
						if status == "Success":
							generos = []
							for genre in genres:
							   generos.append(genre.contents[0].strip())
							actores = []
							for actor in cast:
								actores.append(actor.contents[0].strip())
							movie = {"Title": title, "Year": year, "Rating": rating, "Genres": generos, "Synopsis": synopsis, "Cast": actores, "Site" : 'RottenTomatoes', "Image" : image, "URL" : url}
							scrapercollection.insert(movie)
		return status

def main():
	client = MongoClient()
	db = client.crawlerdb
	db2 = client.scraperdb
	crawlercollection = db.crawlercollection
	scrapercollection = db2.scrapercollection
	log = open('log.txt', 'w')
	while True:
		document = crawlercollection.find_one({"readed" : None})
		if document:
			try:
				if "imdb" in document["url"]:
					print "IMDB"
					status = ScrapingIMDB(document["html"], scrapercollection, document["url"])
					print status
				elif "rottentomatoes" in document["url"]:
					print "RT"
					status = ScrapingRottenTomatoes(document["html"], scrapercollection, document["url"])
					print status
				if status == "Fail":
					document["invalid"] = True
					log.write('El url ' + document["url"] + ' no pudo ser procesado. \n')
				elif status == "Serie":
					document["invalid"] = True
					log.write('El url ' + document["url"] + ' es de una serie. \n')
			except:
				document["invalid"] = True
				log.write('El url ' + document["url"] + ' no pudo ser procesado. \n')
			document["readed"] = True
			document["html"] = ""
			crawlercollection.save(document)
		else:
			time.sleep(10)

if __name__ == '__main__':
	main()
