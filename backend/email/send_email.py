import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from backend.settings import EMAIL_SETTINGS


class Email:
    def __init__(self):
        """Инициализация объекта Email."""
        self.smtp_user = EMAIL_SETTINGS.get('SMTP_USER')

    def setup_connection(self):
        """Установка соединения с SMTP-сервером."""
        smtp_server = EMAIL_SETTINGS.get('SMTP_SERVER')
        smtp_port_str = EMAIL_SETTINGS.get('SMTP_PORT')

        if not smtp_server or not smtp_port_str:
            logging.error(
                "SMTP_SERVER и/или SMTP_PORT отсутствуют в настройках.")
            return None

        try:
            server = smtplib.SMTP(smtp_server, int(smtp_port_str))
            server.starttls()
            server.login(self.smtp_user, EMAIL_SETTINGS.get('SMTP_PASSWORD'))
            return server
        except smtplib.SMTPException as e:
            logging.error(f"Ошибка при установке соединения: {e}")
            return None

    def create_msg(self, subject, body, to):
        """Создание письма."""
        message = MIMEMultipart()
        message['From'] = self.smtp_user
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        return message

    @staticmethod
    def close_connection(server):
        """Закрытие соединения с SMTP-сервером."""
        try:
            server.quit()
        except smtplib.SMTPException as e:
            logging.error(f"Ошибка при закрытии соединения: {e}")

    def send_message(self, subject, body, to):
        """Отправка электронного письма."""
        server = self.setup_connection()
        if not server:
            return

        message = self.create_msg(subject, body, to)

        try:
            server.sendmail(self.smtp_user, to.split(','), message.as_string())
            logging.info("Сообщение успешно отправлено")
        except smtplib.SMTPException as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")
        finally:
            self.close_connection(server)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    email = Email()
    email.send_message(
        subject="Тестовое сообщение", body='test', to='rofel@fm.ru')
