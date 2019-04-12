import requests
import datetime
import time

class User:
    server_address = "http://localhost:5000"

    def __init__(self, server):
        self.server_address = server

    def __init__(self, host, port):
        self.server_address = "http://" + host + ":" + str(port)

    def create_user(self, username, password, email):
        body = {
            "username" : username,
            "password" : password,
            "email" : email,
            "level" : "normal"
        }
        r = requests.post(self.server_address + "/user", json=body, headers={"content-type":"application/json"})
        return r.status_code


    # users = list of usernames
    def create_admin(self, username, password, email, users):
        body = {
            "username" : username,
            "password" : password,
            "email" : email,
            "level" : "admin",
            "users" : users
        }
        r = requests.post(self.server_address + "/user", json=body, headers={"content-type":"application/json"})
        return r.status_code


class Connection:

    server_address = "http://localhost:5000"
    username = ""
    password = ""
    token = ""
    previous_timestamp = None

    def __init__(self, server):
        self.server_address = server

    def get_token(self):
        body = {
            "username" : self.username,
            "password" : self.password
        }
        r = requests.post(self.server_address + "/login-session", json=body, headers={"content-type":"application/json"})
        self.token = r.json()["token"]

    def __init__(self, host, port, username, password):
        self.server_address = "http://" + host + ":" + str(port)
        self.username = username
        self.password = password 
        self.get_token()

    def remove_user(self):
        url = self.server_address + "/user?token=" + self.token + "&username=" + self.username
        r = requests.delete(url)
        return r.status_code

    def publish_message(self, key, message):
        message_body = {
            "text" : message,
            "key" : key,
            "token" : self.token
        }
        head = {"content-type" : "application/json"}
        r = requests.post(url =  self.server_address + "/message", json=message_body, headers=head)
        print (r.json())


    def get_all_messages(self, key):    
        url = self.server_address + "/message?key=" + key + "&token=" + self.token
        r = requests.get(url)
        return r.json()


    def get_message_after(self, key, after_time):
        url = self.server_address + "/message?key=" + key + "&from_time=" + after_time + "&token=" + self.token
        r = requests.get(url)
        return r.json()


    def start_polling(self, key, callback, from_time=None):
        if from_time:
            self.previous_timestamp = from_time
        else:
            self.previous_timestamp = str(datetime.datetime.today())
        while(1):
            messages = self.get_message_after(key, self.previous_timestamp)
            
            try:
                if len(messages) > 0:
                    self.previous_timestamp =  messages[len(messages)-1]["timestamp"]
                    callback(key, messages)
            except:
                print("Topic error")
                break
            time.sleep(0.8)


    def update_scope(self, admin, user, topics):
        url = self.server_address + "/scope"
        body = {
            "admin" : admin,
            "user" : user,
            "topics" : topics,
            "token" : self.token
        }
        r = requests.post(url, json=body, headers={"content-type":"application/json"})
        return r.status_code