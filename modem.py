#!/usr/bin/env python2.7

from __future__ import print_function
from sshhelper import *
from f5helper import *
import logging
import commands

PORT = '/dev/ttyUSB1'
BAUDRATE = 115200
PIN = '0000' # SIM card PIN (if any)
from gsmmodem.modem import GsmModem
CMD_LIST = {'mem': """used=$(free | grep Mem | awk '{print $3/$2 * 100.0}' | sed 's/\./ /g' |awk '{print $1}' | xargs echo);echo "Used Memory: $used%" ; let free=100-$used; echo "Free Memory: $free%"  """,
            'cpu': 'uptime',
            'disk': """ df -h -t ext4| grep -v Filesystem | awk '{print "Size: "$2" Used: "$5" "$6}'| xargs echo "Disk usage " """,
            'bash':""}

# replace this with the ips of the vms
VM_LIST = {'group1': ['first_vm_ip_or_hostname','second_vm_ip_or_hostname'],
           'group2': ['first_vm_ip_or_hostname','second_vm_ip_or_hostname', 'third_vm_ip_or_hostname']}

def readCredentials():
    global ssh_username
    global ssh_password
    global ssh_bastion
    try:
        auth_file = open(os.path.dirname(os.path.realpath(__file__))+"/credentials.json", "r")
        auth_json = json.load(auth_file)
    except Exception as e:
            print("Credentials file error: {}".format(e))
            sys.exit(1)
    ssh_username = auth_json["ssh"]["username"].encode('ascii')
    ssh_password = auth_json["ssh"]["password"].encode('ascii')
    ssh_bastion = auth_json["ssh"]["bastion"].encode('ascii')

def determineCommand(cmd):
    # command[0] is from CMD_LIST
    # command[1] is from VM_LIST
    #print(cmd)
    command = cmd.split()
    if command[0] not in CMD_LIST.keys():
        return ('Command not allowed!')
    else:
        if command[1] not in VM_LIST.keys():
            return ('Inapropriate TLA')
        else:
            #print(VM_LIST[command[1]])
            #print(CMD_LIST[command[0]])
            #print(VM_LIST[command[1]][0])
            #print(type(ssh_bastion)
            return_val = ""
            if command[0] == 'bash':
                for vm in VM_LIST[command[1]]:
                    output = runCommand(ssh_username, ssh_password, ssh_bastion, vm, " ".join(command[2:]))
                    return_val = (return_val + vm + " # " + " ".join(output))
                    print(return_val)
            else:
                for vm in VM_LIST[command[1]]:
                    output = runCommand(ssh_username, ssh_password, ssh_bastion, vm, CMD_LIST[command[0]])
                    return_val = return_val + vm + " # " + " ".join(output)
            return return_val

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    #print((sms.text).encode('ascii'))
    comm = sms.text.lower().split()[0]
    output = determineCommand(sms.text.lower())
    print('replying to SMS...')
    #print(output)
    #print(type(output))
    sms.reply(output)
    print('SMS sent.\n')

def runModem():
    print('Initializing modem...')
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    modem.deleteMultipleStoredSms()
    #modem.sendSms('+44740000000','asdsdefed',False)
    print('Waiting for SMS message...')
    try:
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close();

def main():
    #print('Initializing modem...')
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    #modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    #modem.smsTextMode = False
    #modem.connect(PIN)
    #modem.sendSms('+4474000000','asdsdefed',False)
    #print('Waiting for SMS message...')
    #try:
    #    modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    #finally:
    #    modem.close();
    #prilnt(determineCommand("cpu gmapp"))
    readCredentials()
    runModem()
if __name__ == '__main__':
    main()
