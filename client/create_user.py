from smqc import smqc

user = smqc.User("localhost",5000)
# print(user.create_user("akanksha","password123","akanksha@gmail.com"))
# print(user.create_user("mridulganga","password123","mridul@gmail.com"))
# print(user.create_admin("gopikakini","password123","gopika@gmail.com",["mridulganga", "akanksha"]))



# for removing user
# conn = smqc.Connection("localhost",5000,"mridulganga", "password123")
# conn.remove_user()


# adding scopes
# conn = smqc.Connection("localhost",5000,"gopikakini", "password123")
# topics = ["main.child.topic1", "main.child.topic2"]
# conn.update_scope("gopikakini", "mridulganga", topics)
