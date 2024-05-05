import sys
import re

def log_to_dict(log):
    dict = {'Month': None, 'Day': None, 'Time': None, 'LabSZ': None, 'sshd': None, 'ip': None, 'port': None, 'user': None,
            'message-type': 'Else', 'error': False}
    words = log.split(' ')

    #Month, day, time, LabSZ
    dict['Month'] = words[0]
    dict['Day'] = words[1]
    dict['Time'] = words[2]
    dict['LabSZ'] = words[3]

    #sshd
    sshd = r'sshd\[(\d+)\]'
    match = re.search(sshd, log)
    if match:
        dict['sshd'] = match.group(1)

    #ip
    ip = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(ip, log)
    if match:
        dict['ip'] = match.group(1)

    #port
    port = r'port (\d+)'
    match = re.search(port, log)
    if match:
        dict['port'] = match.group(1)

    #user
    user = r' user (\w+)| user=(\w+)'
    error = r'error:'
    match = re.search(user, log)
    matchEr = re.search(error, log)
    if match and not matchEr:
        dict['user'] = match.group(1)

    #message type
    keyword = (r'(error:|POSSIBLE BREAK-IN ATTEMPT!|Invalid user|Accepted password|invalid user|Connection closed|'
               r'Received disconnect|Failed password|authentication failure)')
    match = re.search(keyword, log)
    if match:
        word = match.group(1)
        if word == 'error:':
            dict['message-type'] = 'Error'
        if word == 'POSSIBLE BREAK-IN ATTEMPT!':
            dict['message-type'] = 'Break-in attempt'
        elif word == 'Accepted password':
            dict['message-type'] = 'Successful login'
        elif word == 'Failed password':
            dict['message-type'] = 'Incorrect password'
        elif word == 'Invalid user' or word == 'invalid user':
            dict['message-type'] = 'Invalid user'
        elif word == 'Connection closed' or word == 'Received disconnect':
            dict['message-type'] = 'Connection closed'
        elif word == 'authentication failure':
            dict['message-type'] = 'Failed login'


    #error
    error = r'(error:)'
    match = re.search(error, log)
    if match:
        dict['error'] = True

    return dict

def get_ipv4s_from_log(dict):
    return dict['ip']

def get_user_from_log(dict):
    return dict['user']

def get_message_type_from_log(dict):
    return dict['message-type']




if __name__ == "__main__":
    input = sys.stdin.readlines()

    for log in input:
        print(log_to_dict(log))