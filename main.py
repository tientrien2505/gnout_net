from sshtunnel import SSHTunnelForwarder, open_tunnel
from time import sleep
import yaml
import logging
from argparse import ArgumentParser, Namespace
import os

OWNER = 'truongdt3'

class CustomNamespace(Namespace):
    owner: str

def parse_arguments() -> CustomNamespace:
    parser = ArgumentParser()
    parser.add_argument('--owner', required=True, type=str, help='program owner')
    return parser.parse_args(namespace=CustomNamespace)

app_path = os.path.join(os.path.expanduser('~'), 'AppData/Local/GnourtNet')
if not os.path.exists(app_path):
    os.mkdir(app_path)

logging.basicConfig(level=logging.ERROR, filename=os.path.join(app_path, 'logs.log'), filemode='a')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    args = parse_arguments()
    if args.owner != OWNER:
        logger.error('Wrong owner')
        raise 'Wrong owner'
    with open('config.yaml', 'r') as f:
        conf = yaml.safe_load(f)
    logger.info(f'Config: {conf}')
    servers = []
    for e in conf:
        server = SSHTunnelForwarder(
            (e['intermediate_host'], e['intermediate_port']),
            ssh_username=e['ssh_username'],
            ssh_password=e.get('ssh_password', None),
            ssh_pkey=e.get('ssh_pkey', None),
            remote_bind_address=(e['remote_bind_address']['host'], e['remote_bind_address']['port']),
            local_bind_address=(e['local_bind_address']['host'], e['local_bind_address']['port'])
        )
        servers.append(server)
    for server in servers:
        server.start()
    try:
        while True:
            sleep(1)
    except Exception as ex:
        logger.error(ex)
        for server in servers:
            server.close()