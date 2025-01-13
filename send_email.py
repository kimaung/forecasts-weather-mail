import smtplib    
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart    
import os    
    
def send_email(subject, body, to_email, from_email, sender_name, password):    
    msg = MIMEMultipart()    
    msg['From'] = f"{sender_name} <{from_email}>"  # Menambahkan nama pengirim  
    msg['To'] = to_email    
    msg['Subject'] = subject    
    
    msg.attach(MIMEText(body, 'html'))    
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:    
        server.starttls()    
        server.login(from_email, password)    
        server.sendmail(from_email, to_email, msg.as_string())    
    
if __name__ == "__main__":    
    subject = "Ramalan Cuaca Hari Ini"    
    with open('email_body.html') as f:    
        body = f.read()    
    to_email = os.getenv('EMAIL_TO')    
    from_email = os.getenv('EMAIL_FROM')    
    sender_name = "Dukun Chabul"
    password = os.getenv('EMAIL_PASSWORD')    
    
    if not body:    
        print("EMAIL_BODY is not set. Exiting.")    
        exit(1)    
    
    send_email(subject, body, to_email, from_email, sender_name, password)    
