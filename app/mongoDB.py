from config import MONGO_DSN
import pymongo
from bson.binary import Binary

client = pymongo.MongoClient({MONGO_DSN}, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")