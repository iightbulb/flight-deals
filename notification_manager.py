from twilio.rest import Client
import smtplib
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.getenv('twilio_account_sid'), os.getenv('twilio_auth_token'))

    def send_sms(self, the_message):
        message = self.client.messages.create(
            body=the_message,
            from_=os.getenv('my_twilio_number'),
            to=os.getenv('my_number')
        )
        print(message.sid)

    def send_email(self, the_message, email_addresses, names):
        with smtplib.SMTP("smtp.gmail.com") as connection: #URL OF EMAIL SERVER
            connection.starttls()
            connection.login(os.getenv('my_email'), os.getenv('my_password'))
            for email in email_addresses:
                for name in names:
                    connection.sendmail(
                    from_addr=os.getenv('my_email'),
                    to_addrs=email,
                    msg=f"Hey {name} \n{the_message}"
                    )
