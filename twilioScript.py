#!/usr/bin/env python3
# Download the helper library from https://www.twilio.com/docs/python/install
# Note Twilio's rate-limiting documentation: https://www.twilio.com/docs/sms/send-messages#a-note-on-rate-limiting
import csv, sys 
import os
import time
from twilio.rest import Client
from dotenv import load_dotenv


MESSAGE_FILE = 'message.txt'     # File containing text message
CSV_FILE = 'participants.csv'    # File containing participant numbers
SMS_LENGTH = 160                 # Max length of one SMS message
MSG_COST = 0.0109                # Cost per message
TIMEOUT_SECONDS = 2              # Sleep time after each text

# Twilio: Find these values at https://twilio.com/user/account
account_sid = os.getenv("ACCOUNT_SID") # Ensure you remove the angle brackets! < >
auth_token =os.getenv("AUTH_TOKEN")
from_num =os.getenv("FROM_NUM ") # 'From' number in Twilio

def trucate_message_for_android(message):
    # length of link to full message is 57 characters
    link_to_full_message = "Read the rest: thesolarpunkproject.com/daily-weather-text"

    shortened_message = message[:90] + "... " + link_to_full_message # total length 151 characters
    # print("Length of shortened message ", len(shortened_message))
    # print("Message for Android users \n", shortened_message)

    if len(shortened_message) > 160: # NOTE: Double check with Mika num of char/bytes
        pass # trigger an alert

    bytes_size = len(shortened_message.encode('utf-8'))
    # print("Message size in bytes ", bytes_size)

    return shortened_message
    

def sendTwilioSMS(message):
    
    # print(message_to_android_users)
    message_to_android_users = trucate_message_for_android(message)
    # How many segments is this message going to use?
    segments = int(len(message_to_android_users.encode('utf-8')) / SMS_LENGTH) +1

    # Open the people CSV and get all the numbers out of it
    with open(CSV_FILE, 'r') as csvfile:
        peoplereader = csv.reader(csvfile)
        numbers = set([p[0] for p in peoplereader]) # remove duplicate numbers
        
    # print(numbers)


    # Calculate how much it's going to cost:
    messages = len(numbers)
    cost = MSG_COST * segments * messages

    # To Do:  log these prints to a file 
    # print("> {} messages of {} segments each will be sent, at a cost of ${} ".format(messages, segments, cost))

    # Check you really want to send them
    # Set up Twilio client
    client = Client(account_sid, auth_token)

    # Send the messages
    for num in numbers:
        # Send the sms text to the number from the CSV file:
        # TODO: test with number
        # print("Sending to " + num)
        client.messages.create(to=num, from_=from_num, body=message_to_android_users)
        time.sleep(TIMEOUT_SECONDS)

    # print("Exiting!")