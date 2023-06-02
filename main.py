from sshtunnel import SSHTunnelForwarder, open_tunnel
from time import sleep
import paramiko


def port_fwd():
    server = SSHTunnelForwarder(
        '10.0.4.124',
        ssh_username="truongdt3",
        ssh_password="basmnjnszk465",
        remote_bind_address=('127.0.0.1', 8097),
        local_bind_address=('localhost', 8097)
    )
    server.start()
    while True:
        sleep(1)

def port_fwd_pro():
    
    with open_tunnel(
        ('10.0.4.124', 22),
        ssh_username="truongdt3",
        ssh_password="basmnjnszk465",
        remote_bind_address=('127.0.0.1', 22),
        local_bind_address=('127.0.0.1', 10022)
    ) as tunnel:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('127.0.0.1', 10022)
        # do some operations with client session
        client.close()

    # while True:
    #     sleep(1)

    print('FINISH!')

if __name__ == '__main__':
    port_fwd_pro()