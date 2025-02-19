import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        # Email configuration (replace with your own)
        email_address = 'support.rajgeotree@geoplanetsolution.in'
        # email_address = os.environ.get('EMAIL_FROM')
        password = 'Shu@1921@1622'
        # password =  os.environ.get('EMAIL_PASS')
        smtp_server = 'smtp.hostinger.com'
        smtp_port = 587  # Use 587 with starttls() instead of 465

        # Create a message
        message = MIMEMultipart()
        message['From'] = email_address
        message['To'] = data['to_email']
        message['Subject'] = 'AtalGPSPL'
        securitycode = data['Link']

        # Plain text content
        text_content = f"""
        Hello,

        This is your security *copy below code:
        {securitycode}

        Please use this code to reset your password. This code is valid for 15 minutes.

        Best regards,
        The GPSPL Team
        """

        # Attach HTML content
        message.attach(MIMEText(text_content, 'plain'))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Use starttls() for secure connection

            # Login to the email account
            server.login(email_address, password)

            # Send the email
            server.sendmail(email_address, [data['to_email']], message.as_string())

            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection in a finally block to ensure it always happens
            if server:
                server.quit()