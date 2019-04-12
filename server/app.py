import datetime
from flask import Flask, request, jsonify
from db import *
app = Flask(__name__)


@app.route("/message", methods=["GET","POST"])
def message_controller():
    
    token = request.get_json()["token"] if request.method == "POST" else request.args.get("token")
    key = request.get_json()["key"] if request.method == "POST" else request.args.get("key")

    if not check_token_expiry(token):
        return jsonify({"status":"token expired"})
    
    username = get_token_username(token)

    if not is_topic_allowed(username, key):
        return jsonify({"status":"topic not in scope"})

    if request.method =="POST":
        content = request.get_json()
        message = content["text"]
        key = content["key"]
        add_message(key, message)
        return jsonify({"status":"success"})
    else:
        if not "key" in request.args:
            return jsonify({"error":"key was not specified."})
        key = request.args["key"]
        if "from_time" in request.args:
            from_time = request.args["from_time"]
            from_time_obj = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S.%f")
            print(from_time_obj)
            messages = get_messages_after(key, from_time_obj)
        else:
            messages = get_messages(key)
        for m in messages:
            m.pop("_id")
            m["timestamp"] = str(m["timestamp"])
        print(messages)
        return jsonify(messages)


@app.route("/login-session", methods=["POST", "DELETE"])
def login_session_controller():
    if request.method == "POST":
        content = request.get_json()
        username = content["username"]
        password = content["password"]
        if verify_password(username, password):
            token = generate_token()
            create_session(username, token)
            return jsonify({
                "username" : username,
                "token" : token
            })
        else:
            return jsonify({"status":"failure"})
    elif request.method == "DELETE":
        token = request.args.get("token")
        destroy_session(token)
        return jsonify({"status":"success"})


@app.route("/user", methods=["POST", "DELETE"])
def user_controller():
    if request.method == "POST":
        content = request.get_json()
        username = content["username"]
        password = content["password"]
        email = content["email"]
        level = content["level"]
        if "users" in  content:
            users = content["users"]
        else:
            users = None
        add_user(username, password, email, level, users)
        return jsonify({"status":"success"})
    elif request.method == "DELETE":
        token = request.args.get("token")
        username = request.args.get("username")
        if check_token_expiry(token):
            if get_token_username(token) == username:
                destroy_session(token)
                remove_user(username)
                return jsonify({"status":"success"})
        return jsonify({"status":"failure"})


@app.route("/scope", methods=["POST"])
def scope_handler():
    content = request.get_json()

    if not check_token_expiry(content["token"]):
        return jsonify({"status":"token expired"})
        
    admin = content["admin"]
    user = content["user"]
    topics = content["topics"]
    update_scopes(admin, user, topics)
    return jsonify({"status":"success"})


if __name__=="__main__":
    app.run()