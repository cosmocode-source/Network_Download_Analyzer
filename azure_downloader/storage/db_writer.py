from storage.mongo_client import metrics_collection

def save_metrics(data):
    metrics_collection.insert_one(data)