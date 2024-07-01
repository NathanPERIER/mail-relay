
from aiosmtplib import SMTP

from email.message import Message
from email.mime.text import MIMEText

from src.utils.named_address import NamedAddress

from typing import Final, Optional



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

    async def _connect(self) -> SMTP :
        conn = SMTP(hostname=self._host, port=self._port, start_tls=False, use_tls=self._starttls)
        await conn.connect()
        if self.authenticated() :
            await conn.login(self._username, self._password)
        return conn

    async def _send_mail(self, to: str, message: str):
        # for line in message.splitlines() :
        #     print(f'> {line}'.rstrip())
        # print()

        conn = await self._connect()

        try:
            await conn.sendmail(self._sender.address, to, message)
        finally:
            await conn.quit()
    
    def send_mail(self, to: str, msg: Message):
        replace_header(msg, 'From', str(self._sender))
        replace_header(msg, 'Reply-To', msg['From'])
        replace_header(msg, 'To', to)

        return self._send_mail(to, msg.as_string())
