Twitter Tweet Scraping
------------
To run this program first run the scraper from the finalProject directory using:

.. code:: bash

    $ scrapy crawl twitter

This generates a twitterData.csv file which is used in the collection of the tweets of users. This project then has a python script using the
twitter API to collect the tweets, run this by:

.. code:: bash

    $ python3 twitterScraping.py

This program takes about 1-2 hours to finish because of twitters rate limiting function. Luckily, the tweepy library has a way around this. 

This program outputs separate csv files for each twitter user according to their name. Take a look at the csvFiles directory for those. 

Let me know if you have any questions. 
