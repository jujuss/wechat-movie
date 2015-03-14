# coding:utf-8

import re


def search(str, pattern):
    p = re.compile(pattern, re.S | re.M)
    m = p.search(str)
    if m:
        return m.group()
    else:
        return None


def finditer(str, pattern):
    p = re.compile(pattern, re.S | re.M)
    return p.finditer(str)
