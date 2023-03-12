from config import MONGO_DSN
import pymongo
from bson.binary import Binary
MONGO_DSN="mongodb://admin:password@127.0.0.1:27017/"
client = pymongo.MongoClient({MONGO_DSN}, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client.files