#! /usr/bin/env python
# coding:utf-8

import config
from movie import app


def main():
    settings = {
    "host": config.server_host,
    "port": config.server_port,
    "debug": True,
    }
    app.run(**settings)

if __name__ == '__main__':
    main()
