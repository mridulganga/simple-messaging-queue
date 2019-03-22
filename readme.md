## Running the Server
```bash
pip3 install -r requirements.txt
python3 app.py
```

    
## Using client

### Making Connection
```python
from smqc import smqc
queue = smqc.Connection("localhost",5000)
```

### Listening Messages
```python
key = input("Enter key: ")
def on_message(key, messages):
	print("NEW Messages")
	for m in messages:
		print(m["key"] + " : " + m["text"])

queue.start_polling(key, on_message)
```

### Publishing Messages
```python
key = input("Enter the key: ")
message = input("Message: ")
queue.publish_message(key, message)
```
