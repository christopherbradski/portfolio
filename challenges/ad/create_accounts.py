from posixpath import split

import csv
from tkinter.ttk import Separator
import names
import os
import random
import string

from pyad import *

AD_ADMINISTRATOR=os.environ.get('AD_ADMINISTRATOR','Administrator')
AD_ADMINISTRATOR_PASS=os.environ.get('AD_ADMINISTRATOR_PASS', 'from the lab')

p = pyad.set_defaults(ldap_server='', username=AD_ADMINISTRATOR, password=AD_ADMINISTRATOR_PASS)

unique_names = {}
sam_length = 7
header_list = ['sam', 'FullName', 'FirstName', 'LastName', 'Password']

words_path = '4_letter_words.txt'

def gen_random_password(words_file_path):
    with open(words_file_path, 'r') as file:
        #words = file.read().splitlines().split(',')
        line = file.read().splitlines()[0]
        words = line.split(',')
    random_words = random.sample(words, 3)
    return '-'.join(random_words) + str(random.randrange(1,8))

def create_user_in_ad(data):
    ou = pyad.adcontainer.ADContainer.from_dn("ou=All_Users, dc=hackerrank, dc=net")
    new_user = pyad.aduser.ADUser.create(data['FirstName'],
        ou,
        data['Password'],
        optional_attributes={
            "displayName": data['FullName'],
            "sam": data['sam'],
            "sn": data['LastName']
        }
    
    )

with open('created_users.csv', 'w') as output:
    w = csv.DictWriter(output, fieldnames=header_list)
    w.writeheader()
    while len(unique_names) < 501:
        user = names.get_full_name()
        sam  = random.choice(string.ascii_lowercase)
        sam += ''.join(random.choices(string.ascii_lowercase + string.digits, k=sam_length))
        unique_names[sam] ={
            'sam': sam,
            'FullName': user,
            'FirstName': user.split(' ')[0],
            'LastName': user.split(' ')[1],
            'Password': gen_random_password(words_path)
        }
        print(sam, unique_names[sam])
        w.writerow(unique_names[sam])
