#!/usr/bin/env python3
from threading import Timer
import scraper


def timer():
    Timer(14400, scraper.database_scrape).start()
