#!/usr/bin/python3

from email.mime.text import MIMEText

from src.mailer import Mailer


def main():
    mailer = Mailer('localhost', 5025, 'test@localhost')
    mailer.send_mail_basic('testuser@example.com', 'Relay test', 'hello')

if __name__ == '__main__' :
    main()
