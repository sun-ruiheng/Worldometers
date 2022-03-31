# Worldometers

I used https://www.worldometers.info/ to try out scheduling crawls with Scrapy's CrawlerRunner.

In a file separate from the main Scrapy.Spider, I added the capability to set a pattern to crawl the page again after an easily changeable amount of time. This file includes multiple types of functions to set various kinds of durations or exact times to crawl again. For example, schedule_next_crawl_tomorrow() would specify a time the next day (and hence every subsequent day) to conduct this crawl again.

Path to Spider:
Worldometers > worldometers > spiders > countries.py

Path to scheduler:
Worldometers > worldometers > spiders > countries_scheduled.py
