#!/usr/bin/env python

import os
import pika
import sys
import time
import json
import argparse

mqrabbit_user = os.getenv("MQRABBIT_USER")
mqrabbit_password = os.getenv("MQRABBIT_PASSWORD")
mqrabbit_host = os.getenv("MQRABBIT_HOST")
mqrabbit_vhost = os.getenv("MQRABBIT_VHOST")
mqrabbit_port = os.getenv("MQRABBIT_PORT")
mqrabbit_exchange = os.getenv("MQRABBIT_EXCHANGE")
mqrabbit_destination = os.getenv("MQRABBIT_DESTINATION")

globalstate = {}

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def send(command, value,
            mqrabbit_user=mqrabbit_user,
            mqrabbit_password=mqrabbit_password, 
            mqrabbit_host=mqrabbit_host,
            mqrabbit_vhost=mqrabbit_vhost,
            mqrabbit_port=mqrabbit_port):

    mqrabbit_credentials = pika.PlainCredentials(mqrabbit_user, mqrabbit_password)
    mqparameters = pika.ConnectionParameters(
        host=mqrabbit_host,
        virtual_host=mqrabbit_vhost,
        port=mqrabbit_port,
        credentials=mqrabbit_credentials)
    
    mqconnection = pika.BlockingConnection(mqparameters)
    channel = mqconnection.channel()

    message = { 'type': command, 'value': value }

    print("Sending: [{0}]".format(json.dumps(message)))
    channel.basic_publish(exchange='', routing_key=mqrabbit_destination, 
                            body=json.dumps(message))
            

        #time.sleep(30)


def main():
    parser = argparse.ArgumentParser(description='Send a command to the rgb unit')
    parser.add_argument('command', type=str)
    parser.add_argument('--string', type=str)
    parser.add_argument('--integer', type=int)
    parser.add_argument('--boolean', type=str2bool)

    args = parser.parse_args()

    print("Found", args)
    if args.command == "active":
        send(args.command, args.boolean)
    elif args.command == "brightness":
        send(args.command, args.integer)
    #readeventsloop(queue=q,condition=writerWaitState)

if __name__ == "__main__":
    main()
