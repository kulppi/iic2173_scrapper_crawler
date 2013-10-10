from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def ScrapingIMDB(path):
	req = Request(path, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req).read()
	soup = BeautifulSoup(BeautifulSoup(page).prettify())
	titleTag = soup.find("span", {"class": "title-extra"})
	if not titleTag:
		titleTag = soup.find("h1", {"class": "header"}).find_all("span")[0]
	titleAux = titleTag.contents[0].strip()
	title = titleAux.replace('\"','')
	year = soup.find("h1", {"class": "header"}).find("a")
	cast = soup.find("table", {"class": "cast_list"}).find_all(itemprop="actor")
	genres = soup.find("div", {"class": "infobar"}).find_all(itemprop="genre")
	synopsis = soup.find("div",{"id": "titleStoryLine"}).find("div",{"itemprop":"description"}).find("p")
	rating = soup.find("div",{"class": "star-box-giga-star"})
	print("Title: " + title)
	print("Year: " + year.contents[0].strip())
	print("Rating IMDB: " + rating.contents[0].strip() + "/10")
	print("Genres: ")
	for genre in genres:
	    print("- " + genre.contents[0].strip())
	print("Synopsis IMDB: " + synopsis.contents[0].strip())
	print("Cast: ")
	for actor in cast:
	    print("- " + actor.a.span.contents[0].strip())

def ScrapingRottenTomatoes(path):
	req = Request(path, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req).read()
	soup = BeautifulSoup(BeautifulSoup(page).prettify())
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
	print("Title: " + title)
	print("Year: " + year)
	print("Genres: ")
	for genre in genres:
	   print("- " + genre.contents[0].strip())
	print("Synopsis RottenTomatoes: " + synopsis.contents[0].strip())
	print("Rating RottenTomatoes: " + rating.contents[0].strip() + "/100")
	print("Cast: ")
	for actor in cast:
	    print("- " + actor.contents[0].strip())

def main():
	while True:
		path = input("Ingrese URL: ")
		if "imdb" in path:
			ScrapingIMDB(path)

		elif "rottentomatoes" in path:
			ScrapingRottenTomatoes(path)


if __name__ == '__main__':
	main()
