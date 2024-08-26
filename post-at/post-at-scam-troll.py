import requests
import os
import random
import string
import json
import re
import time


from pyzufall.person import Person
from faker import Faker

chars = string.ascii_letters + string.digits + '!@#$%^&*()'
random.seed = (os.urandom(1024))


url = 'http://3d1.gmobb.jp/dcm299ccyag4e/bPoistaAG/'


fake = Faker(['de_AT'])

phone_provider_prefix_de_AT = [
    '6991',
    '650',
    '664',
]
# + 7 digit mobile phone number

for x in range(5000):
    responses = []
    req_session = requests.Session() # run a session with persitent cookie ... 
    # form_count = random.randint(1,3) # how much data is provided to the scammers is randomized
    form_count = 3
    #print(f'form_count = {form_count}')
    resp = req_session.get(url)
    search_string=r'.*url=(https://\S+)">' #get the actual url based on the url provieded in the mail
    match = re.search(search_string, resp.text)
    if match:
        scam_url = match.group(1)
    else:
        print("no scam redirect found")
        exit(1)
    resp = req_session.get(scam_url)
    #print(resp.url)

    

    # First Form
    #time.sleep(random.randint(10,180))
    fake_profile = fake.profile()
    fake_password = fake.password()
    print(f"{x:5} -- eMail (s1): {fake_profile['mail']}, Password (s2): {fake_password} ,", end='')
    response = req_session.post(scam_url, allow_redirects=False, data={
    	's1': fake_profile['mail'],
    	's2': fake_password,
    })
    responses.append(response)
    #print(response)
    if form_count == 1:
        continue

    plz=fake_profile['address'].split('\n')[1].split(' ')[0]
    ort=fake_profile['address'].split('\n')[1].split(' ')[1]
    card_expire = fake.credit_card_expire()
    card_expire_mm = card_expire.split('/')[0]
    card_expire_yy = card_expire.split('/')[1]
    card_number = fake.credit_card_number()
    card_cvv = fake.credit_card_security_code()
    # fake.phone_number() doesnt work for austria
    phone = f'{random.choice(phone_provider_prefix_de_AT)}{random.randint(0,9999999):07}'     

    print(f"PLZ (s11): {plz}, Ort (s12): {ort}, Name (s13): {fake_profile['name']}, CardData: {card_number} {card_expire_mm}/{card_expire_yy} CVV: {card_cvv}, phone: {phone}, ", end='')
    response = req_session.post(scam_url, allow_redirects=False, data={
    	's11': plz,
    	's12': ort,
        's13': fake_profile['name'],
        'Straße': '',
        's14': card_number,
        's15': card_expire_mm,
        's16': card_expire_yy,
        's17': card_cvv,
        's18': phone,
    })
    responses.append(response)
    #print(response)
    if form_count == 2:
        continue

    fake_tan = f'{random.randint(0,999999):06}'
    print(f'fake_tan: {fake_tan}', end='')
    response = req_session.post(scam_url, allow_redirects=False, data={
    	's20': fake_tan,
    	's21': fake_tan,
    })
    responses.append(response)
    print(";     Response Codes: ", end='')
    for respo in responses:
        print(f'{respo.status_code} ', end='')
    print("");
    #print(req_session.cookies)
