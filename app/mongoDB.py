from config import MONGO_DSN
import pymongo
import gridfs
#MONGO_DSN="mongodb://admin:password@127.0.0.1:27017/"
connection = pymongo.MongoClient({MONGO_DSN}, serverSelectionTimeoutMS=5000)
db = connection['images']
fs = gridfs.GridFS(db)
# file="C:/Users/serge/Desktop/lama_300px.png"
# with open(file, 'rb') as f:
#     contents = f.read()
# res = fs.put(contents, filename="lama_300px.png")
# print(res)
#
# cursor = db.fs.chunks.find({'files_id': res})
# print(cursor)