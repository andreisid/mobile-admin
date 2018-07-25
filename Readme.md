### Python script to run commands to your linux server through SMS.
* A modem with a sim card needs to be attached to he server
* The setup is as follows:
    * SMS to phone nb ----> Linux workstation running the script(with attached GSM Modem) ------> ssh to bastion defined in the credentials file -------> ssh + run commands on the VM_LIST specified in the SMS 
