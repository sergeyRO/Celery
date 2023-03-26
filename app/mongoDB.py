from config import MONGO_DSN
import pymongo
import gridfs
connection = pymongo.MongoClient({MONGO_DSN}, serverSelectionTimeoutMS=5000)
db = connection['images']
fs = gridfs.GridFS(db)
ImageCollection = db['ImageCollection']