from smqc import smqc

queue = smqc.Connection("http://sample-test-sample-app.1d35.starter-us-east-1.openshiftapps.com","mridulganga", "password123")

key = input("Enter key: ")

def on_message(key, messages):
    print("NEW Messages")
    for m in messages:
        print(m["key"] + " : " + m["text"])

queue.start_polling(key, on_message)