from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["cn_project"]
metrics_collection = db["metrics"]