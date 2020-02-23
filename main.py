import glob
import hashlib
import pymongo
filenames = glob.glob("./*")
print(filenames)
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['littlegit']
collection = db['files']
for filename in filenames:
    with open(filename, 'rb') as inputfile:
        data = inputfile.read()
        if len(list(collection.find({"filename": filename}))) == 0:
            confirm = str(
                input(
                    f"a file created named {filename} do you want to add it? (y/n) "
                )).lower
            if confirm == "y":
                info = {
                    "filename": filename,
                    "hash": hashlib.md5(data).hexdigest()
                }
                collection.insert_one(info)
                print("gitty db updated")
            else:
                continue
        else:
            if list(collection.find({"filename":filename}))[0]['hash'] == hashlib.md5(data).hexdigest() :
                confirm = str(
                    input(
                        f"a file changed named {filename} do you want to add it? (y/n) "
                    )).lower
                if confirm == "y":
                    collection.delete_one({"filename": filename})
                    collection.insert_one({
                        "filename": filename,
                        "hash": hashlib.md5(data).hexdigest()
                    })
                    print("gitty db updated")
