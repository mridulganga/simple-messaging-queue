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
    print(token_record)
    if ((datetime.datetime.today() - token_record["timestamp"]).seconds//3600 > 8):
        destroy_session(token)
        return False
    else:
        return True

def get_token_username(token):
    token_record = db.sessions.find_one({"token":token})
    return token_record["username"]

def generate_token():
    from uuid import uuid4
    rand_token = uuid4()
    return str(rand_token)


def sha_hash(line):
    from hashlib import sha256
    return str(sha256(line.rstrip().encode()).hexdigest())



def add_user(username, password, email, level, users=None):
    if level=="admin":
        db.users.insert_one({
            "username" : username,
            "password" : sha_hash(password),
            "email" : email,
            "level" : level,
            "users" : users
        })
    else:
        db.users.insert_one({
            "username" : username,
            "password" : sha_hash(password),
            "email" : email,
            "level" : level
        })

def remove_user(username):
    db.users.remove({
        "username" : username
    })


def get_user(username):
    return db.users.find_one({"username":username})


def change_user_password(username, newpassword):
    user = get_user(username)
    user["password"] = sha_hash(newpassword)
    db.users.replace_one({"username":username},user)


def verify_password(username, password):
    user = get_user(username)
    if sha_hash(password) == user["password"]:
        return True
    return False


def is_topic_allowed(username, topic):
    scope = db.scopes.find_one({"user":username})
    if scope:
        topics = scope["topics"]
        for t in topics:
            if len(t) == len(topic):
                if t == topic:
                    return True
            else:
                if t == topic[:len(t)]:
                    return True
    return False


def update_scopes(admin, user, topics):
    if not is_admin(admin) or not is_managed_by(admin, user):
        print("NOT ADMIN OR NOT MANAGER" + str(is_admin(admin)) + "  "  + str(is_managed_by(admin, user)))
        return

    record = db.scopes.find_one({
        "$and" : [{"admin":admin},{"user":user}]
    })

    if record:
        record["topics"] = topics
        db.scopes.replace_one({"_id":record["_id"]}, record)
    else:
        db.scopes.insert_one({
            "admin" : admin,
            "user" : user,
            "topics" : topics
        })


def is_admin(username):
    user = db.users.find_one({"username":username})
    if user:
        if user["level"] == "admin":
            return True
    return False

def is_managed_by(admin, user):
    user_record = db.users.find_one({"username":admin})
    if user:
        if user in user_record["users"]:
            return True
    return False

if __name__=="__main__":
    # create_session("akanksha",generate_token())
    print(check_token_expiry(get_token("akanksha")))
    print(get_token("akanksha"))
