
import yaml

from src.mailer import Mailer
from src.handler import RelayHandler


def load_yaml(filepath: str):
    with open(filepath, 'r') as f :
        return yaml.load(f, Loader=yaml.SafeLoader)


class RelayConfig :

    def __init__(self, handler: RelayHandler) :
        self.smtp_port: int = 5025
        self.handler = handler



def load_handler_config(data) -> RelayHandler :
    if 'host' not in data or 'sender' not in data :
        raise RuntimeError('Configuration requires at least server.host and server.sender')
    has_auth = 'auth' in data and 'username' in data['auth'] and 'password' in data['auth']
    starttls = data['starttls'] if 'starttls' in data else has_auth
    port = data['port'] if 'port' in data else (587 if starttls else 25)
    mailer = Mailer(data['host'], port, data['sender'])
    if starttls :
        mailer.starttls()
    if has_auth :
        mailer.auth(data['auth']['username'], data['auth']['password'])
    return RelayHandler(mailer)

def load_config(filepath: str) -> RelayConfig :
    data = load_yaml(filepath)

    handler = load_handler_config(data['server'])
    conf = RelayConfig(handler)

    if 'relay' in data :
        relay_data = data['relay']
        if 'smtp_port' in relay_data :
            conf.smtp_port = relay_data['smtp_port']

    return conf