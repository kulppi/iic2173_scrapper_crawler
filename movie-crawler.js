// Example demonstrating the simple (but less flexible) way of initiating
// a crawler.

var mongojs = require('mongojs');
var db = mongojs('crawlerdb', ['crawlercollection']);
//var db = mongojs('grupo1:iic2173@arqui2.ing.puc.cl/crawlerdb', ['crawlercollection']);

var fs = require('node-fs'),
    url = require('url'),
    Crawler = require("simplecrawler").Crawler

var myCrawlerIMBD = new Crawler("www.imdb.com")
myCrawlerIMBD.initialPath = "/search/title?title_type=feature,tv_movie,short";
//myCrawlerIMBD.interval = 1;
myCrawlerIMBD.maxConcurrency = 100;
myCrawlerIMBD.timeout = 1500;
myCrawlerIMBD.listenerTTL = 1500;



myCrawlerIMBD.on("fetchstart",function(queueItem){
		console.log("Starting request for:",queueItem.url);
	})

myCrawlerIMBD.on("fetchcomplete",function(queueItem, responseBuffer, response) {
    console.log("I just received %s (%d bytes)",queueItem.url,responseBuffer.length);
    console.log("It was a resource of type %s",response.headers['content-type']);
    if(queueItem.url.indexOf("title/tt") != -1 && queueItem.url.indexOf("criticreviews") == -1 && queueItem.url.indexOf("showtimes") == -1)
    {
     db.crawlercollection.save({url:queueItem.url, html:responseBuffer, sitio:"IMDB"});
     //console.log(responseBuffer.toString());
    }

    // Do something with the data in responseBuffer
});
//---------------------------------------------------------------------------
var myCrawlerRT = new Crawler("www.rottentomatoes.com")
myCrawlerRT.initialPath = "/";
//myCrawlerRT.interval = 1;
myCrawlerRT.maxConcurrency = 100;
myCrawlerRT.timeout = 1500;
myCrawlerRT.listenerTTL = 1500;



myCrawlerRT.on("fetchstart",function(queueItem){
        console.log("Starting request for:",queueItem.url);
    })

myCrawlerRT.on("fetchcomplete",function(queueItem, responseBuffer, response) {
    console.log("I just received %s (%d bytes)",queueItem.url,responseBuffer.length);
    console.log("It was a resource of type %s",response.headers['content-type']);
    if(queueItem.url.indexOf("/m/") != -1)
    {
     db.crawlercollection.save({url:queueItem.url, html:responseBuffer, sitio:"Rotten Tomatoes"});
     //console.log(responseBuffer.toString());
    }

    // Do something with the data in responseBuffer
});

myCrawlerIMBD.start();
myCrawlerRT.start();
