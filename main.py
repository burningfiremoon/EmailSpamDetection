import config
import imaplib, email
from transformers import pipeline, AutoTokenizer
# not yet used
import regex as re, codecs, string

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

# email fetching
for num in messages[0].split()[:10][::-1]:
    # Fetch (RFC822) Format
    result, msg = imap.fetch(num, "(RFC822)")

    if result == 'OK' and msg is not None:
        message = email.message_from_bytes(msg[0][1])
        # message contains header info
        # sender, date, subject, body, attachments and etc.

        # Multipart email check:
        if message.is_multipart():
            for part in message.walk():
                contentType = part.get_content_type()
                # to ignore attachments
                contentDisposition = str(part.get("Contnent-Disposition"))

                if contentType == "text/plain" and "attachment" not in contentDisposition:
                    # if there's a text/plain part
                    content = part.get_payload(decode=True)
                    
                    if content: # None check
                        body = content.decode("utf-8")
                        break
        else:
            # Non-multipart email
            content = message.get_payload(decode=True)
            if content: # None check
                body = content.decode("utf-8")
    
        if body is None:
            body = "(No text content found)"

        decodedSubject = email.header.decode_header(message['Subject'])
        subject = decodedSubject[0][0]

        # extra bytes decoding step
        if isinstance(subject, bytes):
            subject = subject.decode(decodedSubject[0][1] or "utf-8")

        print("Subject:", subject)
        print("From:", message["From"])
        print("Date:", message["Date"])
        print("Body:", body)
    else:
        print(f"Skipped {num}, invalid fetch")


