from smqc import smqc

user = smqc.User("http://sample-test-sample-app.1d35.starter-us-east-1.openshiftapps.com")
print("success connection")
# print(user.create_user("akanksha","password123","akanksha@gmail.com"))
# print(user.create_user("mridulganga","password123","mridul@gmail.com"))
# print(user.create_admin("gopikakini","password123","gopika@gmail.com",["mridulganga", "akanksha"]))



# for removing user
# conn = smqc.Connection("localhost",5000,"mridulganga", "password123")
# conn.remove_user()


# adding scopes
conn = smqc.Connection("http://sample-test-sample-app.1d35.starter-us-east-1.openshiftapps.com","gopikakini", "password123")
topics = ["main.child.topic3", "main.child.topic2"]
conn.update_scope("gopikakini", "akanksha", topics)
