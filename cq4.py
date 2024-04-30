#!/usr/bin/env python3

import hashlib
import struct
import os
import sys
import time
import argparse
import json 
import datetime
import subprocess
import base64
from Crypto.Cipher import AES # type: ignore
from datetime import timezone

blockchain_file_path = os.getenv("BCHOC_FILE_PATH", "blockchain.dat")
AES_KEY = b"R0chLi4uLi4uLi4="

def encrypt_id(identifier):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    padded_id = str(identifier).ljust(32)  # Pad to ensure block size is correct
    encrypted_id = cipher.encrypt(padded_id.encode())
    return base64.b64encode(encrypted_id).decode()

def create_blockchain():
    genesis_block = create_block('0'*64, None, None, None, "GENESIS", time.time())
    save_block(genesis_block)

def add_item(case_id, item_id, creator, password):
    if not (case_id and item_id and creator and password):
        print("Error: All arguments for 'add' must be provided.")
        return
    block = create_block(get_last_block_hash(), case_id, item_id, creator, "ADD", time.time())
    save_block(block)
    print_block(block)

def checkout_item(item_id, password):
    if not (item_id and password):
        print("Error: 'item_id' and 'password' must be provided for 'checkout'.")
        return
    block = create_block(get_last_block_hash(), None, item_id, None, "CHECKOUT", time.time())
    save_block(block)
    print_block(block)

def checkin_item(item_id, password):
    if not (item_id and password):
        print("Error: 'item_id' and 'password' must be provided for 'checkin'.")
        return
    block = create_block(get_last_block_hash(), None, item_id, None, "CHECKIN", time.time())
    save_block(block)
    print_block(block)

def remove_item(item_id, reason, password):
    if not (item_id and reason and password):
        print("Error: 'item_id', 'reason', and 'password' must be provided for 'remove'.")
        return
    block = create_block(get_last_block_hash(), None, item_id, None, "REMOVE", time.time())
    save_block(block)
    print_block(block)

def create_block(prev_hash, case_id, item_id, owner, action, timestamp):
    block_data = {
        'prev_hash': prev_hash,
        'case_id': case_id,
        'item_id': item_id,
        'owner': owner,
        'action': action,
        'timestamp': timestamp
    }
    block_hash = hash_block(block_data)
    return (prev_hash, case_id, item_id, owner, action, timestamp, block_hash)

def get_last_block_hash():
    try:
        with open(blockchain_file_path, 'rb') as file:
            file.seek(72, os.SEEK_END) 
            return file.read(64).decode().rstrip('\x00')
    except FileNotFoundError:
        return '0'*64

def save_block(block):
    try:
        with open(blockchain_file_path, 'ab') as file:
            file.write(struct.pack('64s36s36s64s10s10s64s', *block))
    except OSError as e:
        print(f"Failed to save block: {e}")
        sys.exit(1)

def hash_block(block_data):
    block_string = json.dumps(block_data, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def print_block(block):
    print(f"> Added item: {block[2]}")
    print(f"> Status: {block[4]}")
    print(f"> Time of action: {time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime(block[5]))}")

def main():
    parser = argparse.ArgumentParser(description='Blockchain Chain of Custody Command Line Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    subparsers.add_parser('init', help='Initialize the blockchain')

    parser_add = subparsers.add_parser('add', help='Add a new item to the blockchain')
    parser_add.add_argument('case_id', type=str, help='Case ID')
    parser_add.add_argument('item_id', type=int, help='Item ID')
    parser_add.add_argument('creator', type=str, help='Creator ID')
    parser_add.add_argument('password', type=str, help='Creator’s password')

    parser_checkout = subparsers.add_parser('checkout', help='Checkout an item from the blockchain')
    parser_checkout.add_argument('item_id', type=int, help='Item ID')
    parser_checkout.add_argument('password', type=str, help='User password')

    parser_checkin = subparsers.add_parser('checkin', help='Checkin an item back into the blockchain')
    parser_checkin.add_argument('item_id', type=int, help='Item ID')
    parser_checkin.add_argument('password', type=str, help='User password')

    parser_remove = subparsers.add_parser('remove', help='Remove an item from the blockchain')
    parser_remove.add_argument('item_id', type=int, help='Item ID')
    parser_remove.add_argument('reason', type=str, help='Reason for removal')
    parser_remove.add_argument('password', type=str, help='User password')
    
    parser_verify = subparsers.add_parser('verify')
    parser_show_cases = subparsers.add_parser('show cases') #print all
    parser_show_item = subparsers.add_parser('show item')
    parser_show_item.add_argument('case_id')
    

    args = parser.parse_args()
    if args.command == 'init':
        up = subprocess.run(['./network.sh', 'up', 'createChannel', '-c', 'mychannel', '-ca'], cwd='fabric-samples/test-network')
        subprocess.run(['./network.sh', 'deployCC', '-ccn', 'basic', '-ccp', '../asset-transfer-basic/chaincode-typescript/', '-ccl', 'typescript'], cwd='fabric-samples/test-network')
        subprocess.run(['npm', 'start'], cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript')
    elif args.command == 'add':
        #public async CreateAsset(ctx: Context, prev_Hash: string, Timestamp: number, caseID: string, evidenceId: string, State: string, Creator: string, Owner: string, D_length: number, data: string)
        caseID = encrypt_id(args.case_id)
        evidenceID= encrypt_id(args.item_id)
        subprocess.run(['node','app.js','add', datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M%S'), caseID,evidenceID,'CHECKEDIN', args.creator, '',args.password],cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript/dist')
    elif args.command == 'checkout':
        subprocess.run(['node','app.js','checkout',evidenceID,args.password],cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript/dist')
    elif args.command == 'checkin':
        subprocess.run(['node','app.js','checkin',evidenceID,args.password],cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript/dist')
    elif args.command == 'remove':
        evidenceID= encrypt_id(args.item_id)
        subprocess.run(['node','app.js','remove',evidenceID,args.reason,args.password],cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript/dist')
        remove_item(args.item_id, args.reason, args.password)
    elif(args.command == 'verify'):
        subprocess.run(['node','app.js', 'verify'])
    elif(args.command == 'show cases'):
        subprocess.run(['node','app.js','show cases'],cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript/dist')
    elif(args.command == 'show item'):
        caseID = encrypt_id(args.case_id)
        subprocess.run(['node','app.js','show item',caseID],cwd='fabric-samples/asset-transfer-basic/application-gateway-typescript/dist')
    else:
        parser.print_help()
        
        
    

if __name__ == "__main__":
    main()
