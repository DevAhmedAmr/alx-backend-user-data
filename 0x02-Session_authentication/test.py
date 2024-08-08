#!/usr/bin/env python3
""" Main 0
"""


class Myclass:
    pass

    def setAtrr(self, key, value):
        self.__setattr__(key, value)


x = Myclass()
x.setAtrr("mmm", "zzzz")
print((x.__dict__))
