from sshtunnel import SSHTunnelForwarder, open_tunnel
from time import sleep
import yaml
import logging
from argparse import ArgumentParser, Namespace
import os

OWNER = 'truongdt3'

template_conf = '''
- intermediate_host: 10.0.4.124
  intermediate_port: 22
  ssh_username: truongdt3
  ssh_password: example
  remote_bind_address: 
    host: 10.221.180.139
    port: 22
  local_bind_address:
    host: 127.0.0.1
    port: 2225
- intermediate_host: 127.0.0.1
  intermediate_port: 2225
  ssh_username: ubuntu
  ssh_pkey: analytics-prod.pem
  remote_bind_address: 
    host: 54.251.202.212
    port: 22
  local_bind_address:
    host: 127.0.0.1
    port: 2233
'''

class CustomNamespace(Namespace):
    owner: str
    working_dir: str

def parse_arguments() -> CustomNamespace:
    parser = ArgumentParser()
    parser.add_argument('--owner', required=True, type=str, help='program owner')
    parser.add_argument('--working-dir', required=False, default='.', type=str, help='Working dir')
    return parser.parse_args(namespace=CustomNamespace)

def get_logger():
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a', format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s')
    return logging.getLogger(__name__)


if __name__ == '__main__':
    args = parse_arguments()
    if args.owner != OWNER:
        logger.error('Wrong owner')
        raise 'Wrong owner'
    os.chdir(args.working_dir)
    logger = get_logger()
    if not os.path.exists('config.yaml'):
        logger.warning('Config not found')
        with open('config.yaml', 'w') as f:
            f.write(template_conf)
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