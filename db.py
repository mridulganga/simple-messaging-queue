import pymongo
import datetime

client = pymongo.MongoClient('localhost', 27017)
db = client.simple_msgq

def add_message(key, message):
    db.messages.insert_one({
        "text":message,
        "key": key+".",
        "timestamp": datetime.datetime.today()
    })

# gets all messages
def get_messages(key):
    import re
    key += "."
    key = key.replace(".","\.")
    regx = re.compile("^"+key+".*")
    return list(db.messages.find(
            {"key" : regx})
        )

# gets all messages after timestamp
def get_messages_after(key, timestamp):
    import re
    key += "."
    key = key.replace(".","\.")
    regx = re.compile("^"+key+".*")
    return list(db.messages.find(
            {"$and" : [{"key" : regx}, {'timestamp': {'$gt': timestamp}}]}
        ))