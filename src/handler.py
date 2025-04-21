
import logging

from aiosmtpd.smtp import SMTP, Envelope, Session, AuthResult, LoginPassword

from email.parser import Parser

from src.mailer import Mailer

logger = logging.getLogger(f"relay.{__name__}")


class RelayHandler:

    def __init__(self, mailer: Mailer):
        self._mailer = mailer
        self._message_parser = Parser()

    async def handle_RCPT(self, server: SMTP, session: Session, envelope: Envelope, address, _rcpt_options: list[str]):
        logger.debug("Got recipient: %s", address)
        # if not address.endswith('@example.com'):
        #     return '550 5.1.1 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK' # 250 2.1.5 Recipient OK

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope):
        logger.debug("Got %i bytes of data from %s (as %s)", len(envelope.content), session.peer, envelope.mail_from)
        message = envelope.content.decode('utf8', errors='replace')

        # print(f"Message from {envelope.mail_from}")
        # print(f"Message for {envelope.rcpt_tos}")
        # print('Message data:\n')
        # for line in message.splitlines():
        #     print(f"< {line}".rstrip())
        # print('\nEnd of message\n')

        msg = self._message_parser.parsestr(message)
        await self._mailer.send_mail(envelope.rcpt_tos, msg)
        return '250 Message accepted for delivery'


class SingleUserAuthenticator:
    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password

    def __call__(self, server: SMTP, session: Session, envelope: Envelope, mechanism: str, auth_data: LoginPassword) -> AuthResult :
        if mechanism not in ['PLAIN', 'LOGIN'] :
            return AuthResult(success=False)
        print(auth_data)
        return AuthResult(success=True)
