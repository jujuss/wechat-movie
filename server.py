#! /usr/bin/env python
# coding:utf-8

from movie import app
from movie.config import server_host, server_port


def main():
    settings = {
        "host": server_host,
        "port": server_port,
        "debug": True,
    }
    app.run(**settings)

if __name__ == '__main__':
    main()
