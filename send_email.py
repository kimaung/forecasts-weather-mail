import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
  
def send_email(subject, body, to_email, from_email, password):  
    msg = MIMEMultipart()  
    msg['From'] = from_email  
    msg['To'] = to_email  
    msg['Subject'] = subject  
      
    msg.attach(MIMEText(body, 'plain'))  
      
    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.starttls()  
    server.login(from_email, password)  
    text = msg.as_string()  
    server.sendmail(from_email, to_email, text)  
    server.quit()  
  
if __name__ == "__main__":  
    import os  
    subject = "Ramalan Cuaca Hari Ini"  
    body = "Berikut adalah ramalan cuaca hari ini:"  
    to_email = os.getenv('EMAIL_TO')  
    from_email = os.getenv('EMAIL_FROM')  
    password = os.getenv('EMAIL_PASSWORD')  
      
    send_email(subject, body, to_email, from_email, password)  
