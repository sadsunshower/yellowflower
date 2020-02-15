# Code by Nicc
# YellowFlower

# Utility file for handbook module, uses a data class for handbook details

import typing


class HandbookInfo():
    
    def __init__(self, code: str, url: str, title: str, description: str, offering: str, \
            conditions: typing.Optional[str], equivalent: typing.Optional[str], exclusion: typing.Optional[str]):
        self._code = code
        self._url = url
        self._title = title
        self._description = description
        self._offering = offering
        self._conditions = conditions
        self._equivalent = equivalent
        self._exclusion = exclusion
    
    @property
    def code(self) -> str:
        return self._code
    
    @property
    def url(self) -> str:
        return self._url

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def offering(self) -> str:
        return self._offering
    
    @property
    def conditions(self) -> str:
        return self._conditions
    
    @property
    def equivalent(self) -> str:
        return self._equivalent
    
    @property
    def exclusion(self) -> str:
        return self._exclusion