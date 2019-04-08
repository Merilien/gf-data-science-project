# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scrapy
import re
import pandas as pd
from bs4 import BeautifulSoup
from soundtrack.items import SoundtrackItem

class SoundtrackSpider(scrapy.Spider):
    name = "soundtrack_spider"
    ids = []
    performer_pattern = ''
    id_pattern = ''
    
    def __init__(self):
        ids = pd.read_csv("C://ws/netflox/data/sorted_imdb/imdb_sorted_reduced.csv")
        self.ids = ids.tconst
        self.performer_pattern = re.compile("Performed by (.+)\n")
        self.id_pattern = re.compile("(tt\d{7})")
        
    def start_requests(self):
        base_url = "https://www.imdb.com/title/{}/soundtrack?ref_=tt_trv_snd"
        for i in self.ids:
            yield scrapy.Request(url=base_url.format(i))
        
    def parse(self, response):
        item = SoundtrackItem()
        soup = BeautifulSoup(response.body.decode("utf-8"), "html5lib")
        tracks = soup.find_all("div", ["soundTrack soda odd", "soundTrack soda even"])
        artists = []
        for track in tracks:
            artists += re.findall(self.performer_pattern, track.get_text())
            item["soundtrack_artists"] = []
            if artists:
                item["soundtrack_artists"] = [a.strip() for a in artists]
        item["imdbId"]= re.findall(self.id_pattern, response.request.url)[0]
        return item





            