import config
import imaplib, email, regex as re, codecs, string

# Imap4_SSL class instance
imap = imaplib.IMAP4_SSL("imap.gmail.com")
## outlook version:
# imap_url = imaplib.IMAP4_SSL("imap.outlook.com")

USER = config.user_email
PASSWORD = config.password
imap.login(USER, PASSWORD)


# Load
# for i in imap.list()[1]:
#     mailbox = i.decode().split(' "/" ')
#     print(mailbox[0] + " = " + mailbox[1])

# accessing specific mail

imap.select('"INBOX"')
status, messages = imap.search(None, 'UNSEEN')

# (RFC822) Format

for num in messages[0].split()[:10][::-1]:
    # Fetch
    result, msg = imap.fetch(num, "(RFC822)")

    if result == 'OK' and msg is not None:
        message = email.message_from_bytes(msg[0][1])
        # message contains header info
        # sender, date, subject, body, attachments and etc.

        decodedSubject = email.header.decode_header(message['Subject'])
        subject = decodedSubject[0][0]

        # extra bytes decoding step
        if isinstance(subject, bytes):
            subject = subject.decode(decodedSubject[0][1] or "utf-8")

        print("Subject:", subject)
        print("From:", message["From"])
        print("Date:", message["Date"])
    else:
        print(f"Skipped {num}, invalid fetch")
