# Code by Nicc
# YellowFlower

# Utility file for handbook module, handles caching of course information

import asyncio, time

from modules.newhandbook.description import fetch_description
from modules.newhandbook.info import HandbookDetails


cache = {}


class CacheItem():

    def __init__(self, course: HandbookDetails, time: int):
        self._course = course
        self._time = time
    
    @property
    def course(self) -> HandbookDetails:
        return self._course
    
    def expired(self, current_time: int, limit: int) -> bool:
        return current_time - self._time >= limit


def fetch_description_cache(code: str) -> HandbookDetails:
    if code in cache and not cache[code].expired(int(time.time()), 6000):
        return cache[code].course
    else:
        desc = fetch_description(2020, code)
        if desc is not None:
            cache[code] = CacheItem(desc, int(time.time()))
        
        return desc