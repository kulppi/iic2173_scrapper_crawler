# IIC2173 Crawler y Scrapper

Aplicación para el crawling de paginas web, enfocado en IMDB, el cual guarda los resultados en una base de datos en MongoDB. 

Scrapper extrae de IMDB y Rotten tomatoes.

This app supports deploying to DCC server system, and a demo is in fact running live at
[http://arqui2.ing.puc.cl/](http://arqui3.ing.puc.cl/). 


## Instalación 

### Crawler

Se basa en [https://github.com/cgiffard/node-simplecrawler](https://github.com/cgiffard/node-simplecrawler) y necesita tener instalado MongoDB

```bash
# para un seteo básico necesita 
npm install simplecrawler 

# Crear carpetas recursivamente y manejo de archivos:
npm install node-fs 
npm install wrench  
```

### Scrapper

Necesita Python 3.3 and  beautifulsoup4-4.3.1.


## Usage 

### Crawler

```bash
# iniciar
node movie-crawler.js 
```

### Scrapper

Este scrapper recibe links de las páginas IMDB y Rotten Tomatoes. Los link deben ser de la siguiente forma:
- IMDB: [http://www.imdb.com/title/tt0111161/](http://www.imdb.com/title/tt0111161/)
- Rotten Tomatoes: [http://www.rottentomatoes.com/m/shawshank_redemption/](http://www.rottentomatoes.com/m/shawshank_redemption/)


## Miscellany

- MIT license.
- Questions/comments/etc. are welcome.
