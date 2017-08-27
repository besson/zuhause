# Zuhause
A scrapy to help you to find apartments/flats to rent easily in Berlin

## Requirements

* [Python](https://www.python.org)
* [Scrapy](https://scrapy.org)
* [Mongodb](https://www.mongodb.com)
* [Elasticsearch](https://www.elastic.co)

## Set up

1. Install requirements:
```
$ pip install -r requirements.txt
```
2. Set your Mongodb and Elasticsearch configuration of zuhause/zuhause_config.py
3. Make sure Mongodb and Elasticsearch is running :)

## Scrapping apartments
```
$ cd zuhause
$ scrapy crawl <spider name>
```
#### Available spiders
* coming-home

## Searching

1. Set up your search parameters (filters) in a .yml file, like this example:

![filters](http://thecodeknight.herokuapp.com/img/search_filter.png)

2. Run search across your filters:
```
$ python search.py search/my_search.yml
```
