from smqc import smqc


queue = smqc.Connection("https://sample-test-sample-app.1d35.starter-us-east-1.openshiftapps.com","akanksha", "password123")

key = input("Enter the key: ")

while(1):
    message = input("Message: ")
    queue.publish_message(key, message)