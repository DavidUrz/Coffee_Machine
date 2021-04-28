import smtplib
from email.message import EmailMessage

def send_email(subject, body, to, server = "smtp.gmail.com", port = 465):
    EMAIL_ADDRESS = "dvd1493@gmail.com"
    EMAIL_PASSWORD = "junkzzrhhdhaexav"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg.set_content(body)

    if server == "smtp.gmail.com":
        with smtplib.SMTP_SSL(server, port) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(server, port) as smtp:
            smtp.send_message(msg)

# send_email("test3", "local host", "dvd1493@gmail.com", server="localhost", port=1025)
# send_email("test3", "local host", "dvd1493@gmail.com")