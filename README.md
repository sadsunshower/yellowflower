# YellowFlower

Nicc's Discord bot, now "open source" --- at least to people in the UNSW Discord.

I'm guessing most of you are just here to look at the code and possibly use it in your own projects, but for those of you who are interested there are a number of things which need to be done:

## Style

* _Commenting_ - Most of the code is uncommented, to be fair I should really be the one to deal with this since I understand most of the code

* _PEP compliance_ - I still don't actually know what PEP is so I just put two new lines between functions instead of one, I don't think that's all...

* _OOP conversion_ - The command modules (handbook, boredom, cats, etc.) could do with being converted to proper classes

* _Variable naming, etc._ - The code is just generally very messy, again this should probably be my job...

## Handbook

* _Improved search_ - The search could be improved using various other metrics. Some ideas: TF-IDF on keywords in handbook description, uni-directional PageRank-style ratings based on pre-requisites, remembering individual user's preferences

* _Merging search code_ - The search code in C could possibly be moved to Python, the L-D distance computations are made a lot faster using memoisation and should still be fast enough in Python. It helps to have everything in one language. If we can't move the C search code to Python, we should move _all_ the searching logic to C

* _Better course popularity scraping_ - The course popularity scraper (`cuscrape.py` --- scrapes the class utilisation page) is very buggy, but works "well enough"

* _Classutil in search results_ - Provide enrollment / class utilisation information in the handbook information embed. Alternatively, make a separate command for this

## Boredom

* _Other sources_ - We could pull some entertainment from other places on the internet

## Cat Subscriptions

* _Bugs_ - The cat subscription service is very buggy, and hard to test because it happens over very long timespans. We should consider using a proper scheduling library for it and not relying on asyncio

## Other Features

You are welcome to suggest / implement other features and include them in a pull request.

## Where's half the search utilities?

Some of the search utilities are unavailable, because they were used as an integral part of a uni assignment, and my uni loves to re-use assignments for CS courses. So to prevent plagiarism and any such trouble these files have been removed from the public Git repository:

* `combine.c` - Combines a ranking of results from stdin with their ranking in `courses-pop.txt`
* `footrule.c` and `footrule.h` - The logic combining the rankings of results, by minimising the scaled footrule distance.

For people wishing to run this bot for themselves these files may be requested at any time from me (Discord: `Nick_#7324`) under the same licence as the rest of the project.