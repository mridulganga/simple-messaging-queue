import datetime
from flask import Flask, request, jsonify
from db import add_message, get_messages, get_messages_after
app = Flask(__name__)

@app.route("/message", methods=["GET","POST"])
def message_controller():
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
        pass # attempt user login and return access token
    elif request.method == "DELETE":
        pass # logout user and remove access token from system



if __name__=="__main__":
    app.run()