import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

a = "JoeLewis3335@gmail.com"

msg = MIMEMultipart()
message = "Hello"

msg['From'] = a
msg['To'] = "joelewis3335@yahoo.com"
msg['Subject'] = "THIS IS TEST"

msg.attach(MIMEText(message, 'plain'))



p = "Laxlife123"

s = smtplib.SMTP(host='smtp.gmail.com', port='587')
s.starttls()
s.login(a, p)

s.send_message(msg)

