from conversation_processor import Conversation_Processor
from user import User
u=User()
f = open("D:\email.txt", "r")
f1 = f.read().splitlines()
print(f1)
u.set_email_address(f1[0])
u.set_email_password(f1[1])
u.set_name('ASD')
cp=Conversation_Processor(False)
cp.assign_user_object(u)
cp.loop()