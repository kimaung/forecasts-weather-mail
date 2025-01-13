import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
import os  
  
def send_email(subject, body, to_email, from_email, password):  
    msg = MIMEMultipart()  
    msg['From'] = from_email  
    msg['To'] = to_email  
    msg['Subject'] = subject  
      
    msg.attach(MIMEText(body, 'html'))  
      
    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.starttls()  
    server.login(from_email, password)  
    text = msg.as_string()  
    server.sendmail(from_email, to_email, text)  
    server.quit()  
  
if __name__ == "__main__":  
    import os  
    subject = "Ramalan Cuaca Hari Ini"  
    body = open('email_body.html').read()  
    to_email = os.getenv('EMAIL_TO')  
    from_email = os.getenv('EMAIL_FROM')  
    password = os.getenv('EMAIL_PASSWORD')  
      
    if not body:  
        print("EMAIL_BODY is not set. Exiting.")  
        exit(1)  
      
    send_email(subject, body, to_email, from_email, password)  
