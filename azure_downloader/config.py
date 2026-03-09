import os
from pymongo import MongoClient

TEST_SERVERS = [
    {"name": "OVH France", "url": "http://proof.ovh.net/files/100Mb.dat"},
    {"name": "OVH Canada", "url": "http://proof.ovh.ca/files/100Mb.dat"},
    {"name": "Tele2 Sweden", "url": "http://speedtest.tele2.net/100MB.zip"},
    {"name": "ThinkBroadband UK", "url": "http://download.thinkbroadband.com/100MB.zip"},
    {"name": "CacheFly CDN", "url": "http://cachefly.cachefly.net/100mb.test"},
    {"name": "Leaseweb Netherlands", "url": "http://mirror.leaseweb.com/speedtest/100mb.bin"},
    {"name": "Hetzner Germany", "url": "http://speed.hetzner.de/100MB.bin"},
    {"name": "Hetzner Finland", "url": "http://fsn1-speed.hetzner.com/100MB.bin"},
    {"name": "Softlayer Dallas", "url": "http://speedtest.dal05.softlayer.com/downloads/test100.zip"},
    {"name": "Softlayer Frankfurt", "url": "http://speedtest.fra02.softlayer.com/downloads/test100.zip"}
]

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
DOWNLOAD_CHUNK_SIZE = 8192
PING_COUNT = 5
CLIENT_NODE_NAME = "azure_probe"