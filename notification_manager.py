import smtplib
USER = "user"
PASSWORD = "password"

class NotificationManager:
    def send_email(self, recipient, message, link):
        with smtplib.SMTP("smtp.office365.com", port=25) as connection:
            connection.starttls()
            connection.login(user=USER, password=PASSWORD)
            connection.sendmail(from_addr=USER, to_addrs=recipient, msg=f"Subject:Low price alert!\n\n{message}\n\n{link}")


