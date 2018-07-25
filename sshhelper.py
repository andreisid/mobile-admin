#!/usr/bin/env python2.7
import paramiko
import sys
import json
from pprint import pprint
import socket
import os

class ClientSsh:
    def __init__(self, host, user, password, bastion):
        self.host = host
        self.user = user
        self.password = password
        self.bastion = bastion

    def runCommands(self, *commands):
        bastion = paramiko.SSHClient()
        bastion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        bastion.connect(hostname=self.bastion, username=self.user, password=self.password, timeout=10)
        transport = bastion.get_transport()
        dest_addr = (self.host, 22)
        local_addr = ('localhost', 2222)
        channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

        remote_client = paramiko.SSHClient()
        remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_client.connect('localhost', port=2222, username=self.user ,password=self.password, sock=channel)

        commands_out = {}
        for _command in commands:
            stdin, stdout, stderr  = remote_client.exec_command(_command)
            output = stdout.readlines()
            commands_out[_command] = output
        return commands_out



def checkDns(hostname):
    try:
        check = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        check = None

    return check

def runCommand(username, password, bastion, hostname, command):

    bas = paramiko.SSHClient()
    bas.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    bas.connect(hostname=bastion, username=username, password=password, timeout=10)
    #stdin, stdout, stderr = bas.exec_command("pwd")
    #print(stdout.readlines())
    transport = bas.get_transport()
    dest_addr = (hostname, 22)
    local_addr = ('localhost', 2222)
    channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

    remote_client = paramiko.SSHClient()
    remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_client.connect('localhost', port=2222, username=username ,password=password, sock=channel)
    stdin, stdout, stderr = remote_client.exec_command(command)
    return(stdout.readlines())

def main():
    runCommand('test_server_ip_or_host', 'whoami')
if __name__ == '__main__':
    main()

