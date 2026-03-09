from pymongo import MongoClient
import pandas as pd
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["cn_project"]
collection = db["metrics"]

def load_data():
    data = list(collection.find())

    if len(data) == 0:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # ignore incomplete downloads
    if "file_size_MB" in df.columns:
        df = df[df["file_size_MB"] >= 99]
    return df