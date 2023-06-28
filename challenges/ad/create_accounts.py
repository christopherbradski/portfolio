from posixpath import split
import names
import os
import random
import string

#from pyad import *

AD_ADMINISTRATOR=os.environ.get('AD_ADMINISTRATOR','Administrator')
AD_ADMINISTRATOR_PASS=os.environ.get('AD_ADMINISTRATOR_PASS', 'from the lab')

#p = pyad.set_defaults(ldap_server='', username=AD_ADMINISTRATOR, password=AD_ADMINISTRATOR_PASS)

unique_names = {}
sam_length = 7

words_path = '4_letter_words.txt'

def gen_random_password(words_file_path):
    with open(words_file_path, 'r') as file:
        #words = file.read().splitlines().split(',')
        line = file.read().splitlines()[0]
        words = line.split(',')
    random_words = random.sample(words, 3)
    return '-'.join(random_words) + str(random.randrange(1,8))

while len(unique_names) < 501:
    user = names.get_full_name()
    sam  = random.choice(string.ascii_lowercase)
    sam += ''.join(random.choices(string.ascii_lowercase + string.digits, k=sam_length))
    unique_names[sam] ={
        'FullName': user,
        'First': user.split(' ')[0],
        'Last': user.split(' ')[1],
        'Password': gen_random_password(words_path)
    }
    print(sam, unique_names[sam])