'''
NOTE
This is kind of a dummy project to test scheduling of Scrapy Spiders using its CrawlerRunner .addCallback() method.
I attempt to document steps meticulously.
I understand that there are currently some logical gaps, in the sense that it is prone to getting errors.
For example, the schedule_next_crawl_today could receive instructions to run in at a time earlier than current time.

^ ACTUALLY JUST IMPLEMENT AN ERROR CATCHER FOR THIS!
'''



# IMPORTS

# get_project_settings() retrieves all the settings from metadata of a project
from scrapy.utils.project import get_project_settings

# By dealing with the reactor directly while using CrawlerRunner, we have more flexibility and control over recurred crawls
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

import datetime as dt


# The spider is found in a different file. This file deals with its scheduling.
from countries import CountriesSpider


# crawl_job() function does the actual job of crawling with our spider, then returns the yield.
def crawl_job():
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(CountriesSpider)


# crawl() gets called at the start of the program.


def crawl():
    # crawl() is the central function that controls which scheduler function to call.

    # Crawl once first. "Deferred" object returned can be configured to crawl again later, using .addCallback(), passing in time as arguments.
    deferred = crawl_job()
    deferred.addCallback(schedule_next_crawl_in, hour=0, minute=1)
    # Here, we chose schedule_next_crawl_in(), one of several scheduler functions. With the "minute" parameter, the next crawl occurs in 1 hour and 15 minutes.

    deferred.addErrback(catch_error)


# Below are different scheduler functions. I hope this is a good naming system that is consistent and intuitive to use.
# When calling one of these scheduler functions, arguments passed into their parameters dictate how much time exactly to wait before next crawl. 
# Currently there are only three of them.


def schedule_next_crawl_in(null, hour, minute=0, second=0):
    # This function calls the spider again in the numbers of hours (compulsory), minutes and seconds (optional) specified as arguments.

    # sleep_time is number of seconds before next crawl.
    sleep_time = 3600*hour + 60*minute + second

    reactor.callLater(sleep_time, crawl)


def schedule_next_crawl_today(null, minute):
    # This function calls the spider again at a specified time on the same day.

    next_time = dt.datetime.now().replace(minute=minute)

    # To find the duration the spider should wait for, take next time minus present time.
    sleep_time = (next_time - dt.datetime.now()).total_seconds()

    reactor.callLater(sleep_time, crawl_job)
    # Here I call crawl_job and not crawl, as I do not want further recurrence — it wouldn't make sense.


def schedule_next_crawl_tomorrow(null, hour, minute):
    # This function calls the spider again at a specified time on the next day.

    # The "tomorrow" variable represents the specific time tomorrow.
    tomorrow = (
        dt.datetime.now() + dt.timedelta(days=1)
    ).replace(hour=hour, minute=minute, second=0, microsecond=0)

    # To find the duration the spider should wait for, take next time minus present time.
    sleep_time = (tomorrow - dt.datetime.now()).total_seconds()

    reactor.callLater(sleep_time, crawl)



def catch_error(failure):
    print(failure.value)


if __name__ == "__main__":
    crawl()
    reactor.run()