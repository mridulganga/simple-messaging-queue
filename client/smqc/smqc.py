import requests
import datetime
import time

class Connection:

    server_address = "http://localhost:5000"
    previous_timestamp = None

    def __init__(self, server):
        self.server_address = server

    def __init__(self, host, port):
        self.server_address = "http://" + host + ":" + str(port)


    def publish_message(self, key, message):
        message_body = {
            "text" : message,
            "key" : key
        }
        head = {"content-type" : "application/json"}
        r = requests.post(url =  self.server_address + "/message", json=message_body, headers=head)
        print (r.json())


    def get_all_messages(self, key):    
        url = self.server_address + "/message?key=" + key
        r = requests.get(url)
        return r.json()


    def get_message_after(self, key, after_time):
        url = self.server_address + "/message?key=" + key + "&from_time=" + after_time
        r = requests.get(url)
        return r.json()


    def start_polling(self, key, callback, from_time=None):
        if from_time:
            self.previous_timestamp = from_time
        else:
            self.previous_timestamp = str(datetime.datetime.today())
        while(1):
            messages = self.get_message_after(key, self.previous_timestamp)
            if len(messages) > 0:
                self.previous_timestamp =  messages[len(messages)-1]["timestamp"]
                callback(key, messages)
            time.sleep(0.8)
