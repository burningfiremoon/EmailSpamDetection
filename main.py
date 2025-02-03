import config
import imaplib, email, regex as re, codecs, string

# Imap4_SSL class instance
imap = imaplib.IMAP4_SSL("imap.gmail.com")
## outlook version:
# imap_url = imaplib.IMAP4_SSL("imap.outlook.com")

user = config.user_email
password = config.password
imap.login(user, password)


# Load
for i in imap.list()[1]:
    mailbox = i.decode().split(' "/" ')
    print(mailbox[0] + " = " + mailbox[1])