#!/usr/bin/env python3

import os
import sys
import time
import pickle
import subprocess
from slack import slack_message

os.system('clear')

try:
    from termcolor import cprint
except:
    sys.exit('[!] Termcolor library not found. Please install before proceeding: pip install termcolor\n')
try:
    from pyfiglet import figlet_format
except:
    sys.exit('[!] Pyfiglet library not found. Please install before proceeding: pip install pyfiglet\n')
try:
    from ecdsa import SigningKey, SECP256k1
except:
    sys.exit('[!] ECDSA library not found. Please install before proceeding: pip install ecdsa\n')
try:
    import requests
except:
    sys.exit('[!] Requests library not found. Please install before proceeding: pip install requests\n')
try:
    import sha3
except:
    sys.exit('[!] Sha3 library not found. Please install before proceeding: pip install sha3\n')

def header():
	cprint(figlet_format('key-monster',font='slant'),'blue')

def key_gen():
    global private
    global addr
    keccak=sha3.keccak_256()
    priv=SigningKey.generate(curve=SECP256k1)
    pub=priv.get_verifying_key().to_string()
    keccak.update(pub)
    addr=keccak.hexdigest()[24:]
    private=priv.to_string().hex()

# todo: optimize by removing file write/read

def store_pairs():
    with open('wallets','ab') as f:
        pickle.dump(pairs,f,protocol=pickle.HIGHEST_PROTOCOL)

def read_pairs():
    with open('wallets','rb') as f:
        data=pickle.load(f)

def check_balance():
    read_pairs()
    for private,addr in pairs.items():
        fetch(addr,private)

def fetch(addr,private):
    api_key=os.environ['ETHERSCAN_API_KEY']
    url='https://api.etherscan.io/api?module=account&action=balance&address=0x{0}&tag=latest&apikey={1}'.format(addr,api_key)
    time.sleep(0.25) # conservative delay to stay within allowed [5] QPS limitation of Etherscan API 
    r=requests.get(url)
    data=r.json()
    bal=data['result']
    print('Address: {0}\nPrivate: {1}'.format(addr,private))
    print('Balance: ${0}'.format(bal))

    # win logic

    if int(bal) is not 0:
        cprint('SUCCESS!\n','green')
        slack_message('[*] Success! Balance: {0} Private: {1}'.format(bal,private))
    else:
        cprint('[!] No dice\n','red')

def main():
    subprocess.run(['rm','wallets'],stdout=subprocess.PIPE)
    subprocess.run(['rm','-r','__pycache__'],stdout=subprocess.PIPE)
    global pairs
    pairs={}
    header()
    num=int(input('Enter number of private keys to generate: '))

    cprint('Generating..\n','cyan')

    i=0
    while(i<num):
        key_gen()
        pairs[private]=addr
        i+=1
    cprint('Done\n','green') 
    cprint('Checking balances..\n','red')
    store_pairs()
    check_balance()
    cprint('Done','green') 

### MAIN ###
if __name__=='__main__':
    main()

