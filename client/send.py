from smqc import smqc


queue = smqc.Connection("localhost",5000, "mridulganga", "password123")

key = input("Enter the key: ")

while(1):
    message = input("Message: ")
    queue.publish_message(key, message)