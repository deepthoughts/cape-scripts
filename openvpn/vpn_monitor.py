import subprocess
import time
import os

def connect_vpn(vpn_conf):
    args = 'openvpn --config {} &'.format(vpn_conf)
    vpn_name = vpn_conf.split('_')[0]
    ph = subprocess.Popen(args,
            shell = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE)
    out, err = ph.communicate()
    print('Attempting to start vpn {}'.format(vpn_name))
    print(out.decode())
    print(err.decode())
    print('vpn {} executed with pid {}'.format(vpn_name, vpn_pid))
    return vpn_name

def disconnect_vpn(vpn_name):
    args = 'ps aux | grep {}'.format(vpn_name)
    ph = subprocess.Popen(args,
            shell = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE)
    out, err = ph.communicate()
    if out:
        for line in out.split(b'\n'):
            vpn_pid = None
            if line.decode().find('openvpn --config {}'.format(vpn_name)) != -1:
                vpn_pid = int(line.split()[1].decode())
                print('Trying to kill {} with pid {}'.format(vpn_name, vpn_pid))
                try:
                    os.kill(int(vpn_pid), 9)
                    print('Sucessfully Terminated {} with pid {}'.format(vpn_name, vpn_pid))
                except ProcessLookupError:
                    print('No such process with PID {}'.format(vpn_pid))
                except:
                    print('Could not kill the process with PID {}'.format(vpn_pid))
    else:
        print('Could not get PID for VPN {}'.format(vpn_name))

def check_vpn_connection(vpn_name):
    args = 'ping 8.8.8.8 -I {} -c 4'.format(vpn_name)
    ph = subprocess.Popen(args,
            shell = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE)
    out, err = ph.communicate()
    if out:
        for line in out.split(b'\n'):
            if line.startswith(b'4 packets transmitted'):
                pkts_recv = int(line.split(b',')[1].split()[0].strip().decode())
                if pkts_recv == 4:
                    print('{0} still up, sleeping...'.format(vpn_name))
                    return True
                elif pkts_recv == 0:
                    print('{0} down, restarting {0}...'.format(vpn_name))
                    return False
    elif err:
        print('err: '+err.decode())
        print('{0} down, restarting {0}...'.format(vpn_name))
        return False
    else:
        print('{0} down, restarting {0}...'.format(vpn_name))
        return False

def main():
    vpn_confs =['tun8_name1.ovpn', 'tun9_name2.ovpn']
    vpn_info = {}
    for conf in vpn_confs:
        vpn_info[conf] = connect_vpn(conf)
    time.sleep(60*60)
    while True:
        for conf in vpn_info:
            if check_vpn_connection(vpn_info[conf]):
                pass
            else:
                disconnect_vpn(vpn_info[conf])
                vpn_info[conf] = connect_vpn(conf)
            time.sleep(10)
        time.sleep(60*60)


if __name__ == "__main__":
    main()
