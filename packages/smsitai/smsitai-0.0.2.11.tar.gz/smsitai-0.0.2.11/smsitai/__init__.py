import json
import requests
import re

USE_SPECIFIED = 0
USE_ALL_DEVICES = 1
USE_ALL_SIMS = 2


def get_phone_number(phone_number):
    if type(phone_number) is str:
        phone_number=re.sub('[^0-9]','',phone_number)
    if type(phone_number)!=int:
        phone_number=int(phone_number)
    if len(str(phone_number))==10:
        return phone_number
    else:
        raise ValueError(f'the proposed phone number is {len(str(phone_number))} digits')

class SMSit:
    def __init__(self, api_key):
        self.server = 'https://www.smsit.ai/smsgateway'
        self.api_key = api_key
        self.send_url = f'{self.server}/services/send.php'
        self.check_messages_url = f'{self.server}/services/read-messages.php'
        self.resend_url = f'{self.server}/services/resend.php'
        self.manage_contacts_url=f'{self.server}/services/manage-contacts.php'
        self.urls=dict(send=f'{self.server}/services/send.php',
                       check_messages=f'{self.server}/services/read-messages.php',
                       resend=f'{self.server}/services/resend.php',
                       manage_contacts=f'{self.server}/services/manage-contacts.php')

    def send_message(self, number, message, schedule=None, devices=0, isMMS=False, attachments=None, prioritize=False):
        message_type = 'mms' if isMMS else 'sms'
        message_priority = 1 if prioritize else 0
        number = get_phone_number(number)
        print(f'number: {number}\nmessage: {message}')
        post_data = dict(number=number,
                         message=message,
                         schedule=schedule,
                         key=self.api_key,
                         devices=devices,
                         type=message_type,
                         attachments=attachments,
                         prioritize=message_priority)
        response = self.send_request(self.send_url, data=post_data)
        return response['messages']

    def send_messages(self, messages, option=USE_SPECIFIED, devices=[], schedule=None, use_random_device=False):
        for m in messages:
            m['number'] = get_phone_number(m['number'])
        post_data = dict(messages=json.dumps(messages),
                         schedule=schedule,
                         key=self.api_key,
                         devices=devices,
                         option=option,
                         use_random_device=use_random_device)
        response = self.send_request(self.send_url, data=post_data)
        return response['data']['messages']

    def get_message_by_id(self, message_id):
        post_data = dict(key=self.api_key,
                         id=message_id)
        response = self.send_request(self.check_messages_url, post_data)
        return response['messages'][0]

    def get_messages_by_group_id(self, group_id):
        post_data = dict(key=self.api_key,
                         groupId=group_id)
        response = self.send_request(self.check_messages_url, post_data)
        return response['messages']

    def get_messages_by_status(self, status, start_timestamp, end_timestamp):
        post_data = dict(key=self.api_key,
                         status=status,
                         startTimestamp=start_timestamp,
                         endTimestamp=end_timestamp)
        response = self.send_request(self.check_messages_url, post_data)
        return response['messages']

    def resend_message_by_id(self, message_id):
        post_data = dict(key=self.api_key,
                         id=message_id)
        response = self.send_request(self.resend_url, post_data)
        return response['messages'][0]

    def resend_messages_by_group_id(self, group_id, status=''):
        post_data = dict(key=self.api_key,
                         groupId=group_id,
                         status=status)
        response = self.send_request(self.resend_url, post_data)
        return response['messages']

    def resend_messages_by_status(self, status, start_timestamp=None, end_timestamp=None):
        post_data = dict(key=self.api_key,
                         status=status,
                         startTimestamp=start_timestamp,
                         endTimestamp=end_timestamp)
        response = self.send_request(self.resend_url, post_data)
        return response['messages']

    def add_contact(self, list_id, number, name=None, resubscribe=False):
        post_data = dict(key=self.api_key,
                         listId=list_id,
                         number=number,
                         name=name,
                         resubscribe=resubscribe)
        response = self.send_request(self.manage_contacts_url, post_data)
        return response['contact']

    def unsubscribe_contact(self, list_id, number):
        post_data = dict(key=self.api_key,
                         listId=list_id,
                         number=number,
                         unsubscribe=True)
        response = self.send_request(self.manage_contacts_url, post_data)
        return response['contact']

    def get_remaining_balance(self):
        response = self.send_request(self.send_url, dict(key=self.api_key))
        credits = response['credits']
        return credits

    def send_request(self, url, data):
        r = requests.post(url, data=data)
        response = r.json()
        print(f'response: {response}')
        return response


