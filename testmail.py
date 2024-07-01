#!/usr/bin/python3

from datetime import datetime, timezone

from smtplib import SMTP

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SimpleMailer :

    def __init__(self, host: str, port: int, sender: str):
        self._host = host
        self._port = port
        self._sender = sender
        self._to: list[str] = []

    def add_recipient(self, to: str):
        self._to.append(to)

    def send(self):
        msg = MIMEMultipart()
        msg['Date'] = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000 (UTC)')
        msg['From'] = self._sender
        msg['Reply-To'] = msg['From']
        msg['To'] = ", ".join(self._to)
        msg['Subject'] = 'Relay test'
        msg.preamble = msg['Subject']
        msg.attach(MIMEText('Hello o/', 'plain', 'utf-8'))

        conn = SMTP(host = self._host, port = self._port)
        try :
            conn.sendmail(self._sender, self._to, msg.as_string())
        finally :
            conn.quit()


def main():
    mailer = SimpleMailer('localhost', 5025, 'test@localhost')
    mailer.add_recipient('testuser@example.com')
    mailer.send()

if __name__ == '__main__' :
    main()
