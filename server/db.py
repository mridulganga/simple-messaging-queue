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

def create_session(username, token):
    db.sessions.insert_one({
        "username": username,
        "token" : token,
        "timestamp" : datetime.datetime.today()
    })

def destroy_session(token):
    db.sessions.remove({"token": token})

# only for test
def get_token(username):
    o = db.sessions.find_one({"username":username})
    if o:
        return o["token"]
    else: 
        return None

def check_token_expiry(token):
    token_record = db.sessions.find_one({"token":token})
    if ((datetime.datetime.today() - token_record["timestamp"]).seconds//3600 > 8):
        destroy_session(token)
        return False
    else:
        return True


def generate_token():
    from uuid import uuid4
    rand_token = uuid4()
    return rand_token


add_user
remove_user




if __name__=="__main__":
    # create_session("akanksha",generate_token())
    print(check_token_expiry(get_token("akanksha")))
    print(get_token("akanksha"))
