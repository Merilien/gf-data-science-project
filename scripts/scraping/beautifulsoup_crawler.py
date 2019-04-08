from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd

def parse_tracks(imdbId):
    url = "https://www.imdb.com/title/{}/soundtrack?ref_=tt_trv_snd".format(imdbId)
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, "html5lib")
    tracks =  soup.find_all("div", ["soundTrack soda odd", "soundTrack soda even"])
    performers = []
    for track in tracks:
        performers += re.findall(pattern, track.get_text())
    d = {"imdbId" : imdbId, "performers" : [p.strip() for p in performers]}
    for p in d["performers"]:
            if p not in artists:
                artists.append(p)
    return d

def crawl_pages(to_crawl):
    for imdbId in to_crawl:
        d = parse_tracks(imdbId)
        data.append(d) 

ids = pd.read_csv("C://ws/netflox/data/ml-20m/links.csv", usecols=["imdbId"])
ids.imdbId = ids.imdbId.map(lambda id: "tt" + (7-len(str(id)))*"0" + str(id))
#set chunk
to_crawl = ids.imdbId[0:100]

artists = []
data = []
pattern = re.compile("Performed by (.+)\n")

crawl_pages(to_crawl)

df = pd.DataFrame(data)
df.to_csv("soundtracks.csv", mode='a', sep=';')  