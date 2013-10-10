// Example demonstrating the simple (but less flexible) way of initiating
// a crawler.

var mongojs = require('mongojs');
var db = mongojs('crawlerdb', ['crawlercollection']);
//var db = mongojs('grupo1:iic2173@arqui2.ing.puc.cl/crawlerdb', ['crawlercollection']);

var fs = require('node-fs'),
    url = require('url'),
    Crawler = require("simplecrawler").Crawler

var myCrawler = new Crawler("www.imdb.com")
myCrawler.initialPath = "/search/title?title_type=feature,tv_movie,short";
//myCrawler.interval = 1;
myCrawler.maxConcurrency = 100;
myCrawler.timeout = 1500;
myCrawler.listenerTTL = 1500;



myCrawler.on("fetchstart",function(queueItem){
		console.log("Starting request for:",queueItem.url);
	})

myCrawler.on("fetchcomplete",function(queueItem, responseBuffer, response) {
    console.log("I just received %s (%d bytes)",queueItem.url,responseBuffer.length);
    console.log("It was a resource of type %s",response.headers['content-type']);
    if(queueItem.url.indexOf("title/tt") != -1)
    {
     db.crawlercollection.save({url:queueItem.url, html:responseBuffer});
     //console.log(responseBuffer.toString());
    }

    // Do something with the data in responseBuffer
});

myCrawler.start();
