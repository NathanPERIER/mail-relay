#!/usr/bin/python3

import argparse
import sys

from getpass import getpass
from datetime import datetime, timezone
from typing import Optional

from smtplib import SMTP

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class LoginInfo:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class SimpleMailer :

    def __init__(self, host: str, port: int, sender: str, login: Optional[LoginInfo]):
        self._host = host
        self._port = port
        self._sender = sender
        self._login = login
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
        msg['Message-ID'] = '<81ddd157-dd19-4561-a113-798b54f5a07d@example.com>'
        msg.preamble = msg['Subject']
        msg.attach(MIMEText('Hello o/', 'plain', 'utf-8'))

        conn = SMTP(host = self._host, port = self._port)
        try :
            if self._login is not None :
                conn.login(self._login.username, self._login.password)
            conn.sendmail(self._sender, self._to, msg.as_string())
        finally :
            conn.quit()


def main():
    parser = argparse.ArgumentParser(description='Simple SMTP relay test script.')
    parser.add_argument('-s', '--host', nargs=1, help='hostname of the SMTP server', default='localhost')
    parser.add_argument('-p', '--port', nargs=1, help='port of the SMTP server', type=int, default='5025')
    parser.add_argument('-u', '--user', nargs=1, help='username for SMTP login', default='')
    parser.add_argument('-f', '--from', nargs=1, help='email address to use for the sender', default='testuser@localhost', dest='frm', metavar='FROM')
    parser.add_argument('dest', nargs='+', help='email addresses to which the mail will be sent')
    args = parser.parse_args(sys.argv[1:])

    login = None
    if len(args.user) > 0 :
        password = getpass('Auth password > ')
        login = LoginInfo(args.user, password)
    mailer = SimpleMailer(args.host, args.port, args.frm, login)
    for dest_addr in args.dest :
        mailer.add_recipient(dest_addr)
    mailer.send()

if __name__ == '__main__' :
    main()
