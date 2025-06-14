#!/usr/bin/python3

import argparse
import sys

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
        msg['Message-ID'] = '<81ddd157-dd19-4561-a113-798b54f5a07d@example.com>'
        msg.preamble = msg['Subject']
        msg.attach(MIMEText('Hello o/', 'plain', 'utf-8'))

        conn = SMTP(host = self._host, port = self._port)
        try :
            conn.sendmail(self._sender, self._to, msg.as_string())
        finally :
            conn.quit()


def main():
    parser = argparse.ArgumentParser(description='Simple SMTP relay test script.')
    parser.add_argument('-s', '--host', nargs=1, help='hostname of the SMTP server', default='localhost')
    parser.add_argument('-p', '--port', nargs=1, help='port of the SMTP server', type=int, default='5025')
    parser.add_argument('-f', '--from', nargs=1, help='email address to use for the sender', default='testuser@localhost', dest='frm', metavar='FROM')
    parser.add_argument('dest', nargs='+', help='email addresses to which the mail will be sent')
    args = parser.parse_args(sys.argv[1:])

    mailer = SimpleMailer(args.host, args.port, args.frm)
    for dest_addr in args.dest :
        mailer.add_recipient(dest_addr)
    mailer.send()

if __name__ == '__main__' :
    main()
