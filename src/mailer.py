
from smtplib import SMTP, SMTP_SSL

from email.message import Message
from email.mime.text import MIMEText

from src.utils.named_address import NamedAddress

from typing import Final, Optional

# TODO iosmtplib ?


def replace_header(msg: Message, header: str, value: str):
    if header in msg :
        msg.replace_header(header, value)
    else :
        msg[header] = value

class Mailer :

    def __init__(self, host: str, port: int, sender: str):
        self._host: Final[str] = host
        self._port: Final[str] = port
        self._sender: Final[NamedAddress] = NamedAddress('Mail-Relay', sender)
        self._starttls: bool = False
        self._username: Optional[str] = None
        self._password: Optional[str] = None
    
    def starttls(self):
        self._starttls = True

    def secure(self) -> bool :
        return self._starttls
    
    def auth(self, username: str, password: str):
        self._username: Optional[str] = username
        self._password: Optional[str] = password
    
    def authenticated(self) -> bool :
        return self._username is not None and self._password is not None
    
    def _connect(self) -> "SMTP|SMTP_SSL" :
        if self._starttls :
            conn = SMTP_SSL(host = self._host, port = self._port)
        else :
            conn = SMTP(host = self._host, port = self._port)
        conn.set_debuglevel(False)
        if self.authenticated() :
            conn.login(self._username, self._password)
        return conn

    def _send_mail(self, to: str, message: str):
        # for line in message.splitlines() :
        #     print(f'> {line}'.rstrip())
        # print()

        conn = self._connect()

        try:
            conn.sendmail(self._sender.address, to, message)
        finally:
            conn.quit()
    
    def _from_addr(self) -> str :
        return 
    
    def send_mail(self, to: str, msg: Message):
        replace_header(msg, 'From', str(self._sender))
        replace_header(msg, 'Reply-To', msg['From'])
        replace_header(msg, 'To', to)

        self._send_mail(to, msg.as_string())
    
    def send_mail_basic(self, to: str, subject: str, content: str, mime_subtype: str = 'plain'):
        msg = MIMEText(content, mime_subtype, 'utf-8')
        msg['From'] = str(self._sender)
        msg['Reply-To'] = msg['From']
        msg['To'] = to
        msg['Subject'] = subject

        self._send_mail(to, msg.as_string())
