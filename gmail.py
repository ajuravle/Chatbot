import imaplib     
import json
import email

def get_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()



obj = imaplib.IMAP4_SSL('imap.gmail.com', 993)    
obj.login('chadbotb1', 'chadbotb12016')
obj.list()
obj.select('inbox') 

result, data = obj.search(None, 'FROM', '"Monica Vizitiu"')
 
ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest
 
result, data = obj.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
 
raw_email = data[0][1]

email_message = email.message_from_string(raw_email.decode("UTF-8"))

#print(email_message['To'])
#print(email_message.items())

message = get_text_block(email_message)

print(message)

