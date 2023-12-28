import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


class Email:

    def __init__(self):
        """Инициализация объекта Email."""
        load_dotenv()

        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.to_email = os.getenv('TO_EMAIL')

    def setup_connection(self):
        """Установка соединения с почтовым сервером."""
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.smtp_user, self.smtp_password)
        except smtplib.SMTPException as e:
            print(f"Ошибка при установке соединения: {e}")

    def send_message(self, subject, body):
        """Отправка сообщения. Текст письма."""
        try:
            message = MIMEMultipart()
            message['From'] = self.smtp_user
            message['To'] = self.to_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            self.server.sendmail(self.smtp_user,
                                 self.to_email,
                                 message.as_string())
        except smtplib.SMTPException as e:
            print(f"Ошибка при отправке сообщения: {e}")

    def close_connection(self):
        """Закрытие соединения с почтовым сервером."""
        try:
            self.server.quit()
        except smtplib.SMTPException as e:
            print(f"Ошибка при закрытии соединения: {e}")


if __name__ == "__main__":
    email_client = Email()

    try:
        email_client.setup_connection()
        subject = "Тестовое сообщение"
        body = "Тест."
        email_client.send_message(subject, body)
        print("Тестовое сообщение отправлено успешно.")
    finally:
        email_client.close_connection()
