import requests
import re
from bs4 import BeautifulSoup
import csv
import os
import pyDes


def create_user_data():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + "user_data.csv"

    if not os.path.isfile(file_path):
        print('Enter your number: ')
        NUMBER = input().encode('utf-8')
        print('Enter passcode: ')
        CODE = input().encode('utf-8')
        k = pyDes.des(b"DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        CODE = k.encrypt(CODE)

        data = [[NUMBER], [CODE]]
        with open('user_data.csv', "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(data)


def delete_user_data():
    os.remove('./user_data.csv')


def login_data():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + "user_data.csv"
    with open(file_path, "rb") as f:
        CODE = f.read()

    NUMBER_t = re.findall(b"'(.*?)'", CODE, re.DOTALL)
    NUMBER = NUMBER_t[0].decode()
    CODE = NUMBER_t[1]
    CODE = CODE.decode('unicode-escape').encode('ISO-8859-1')  # encoding adds extra backslashes and this removes them

    k = pyDes.des(b"DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    CODE = k.decrypt(CODE).decode()
    return [NUMBER, CODE]


def login_three(NUMBER, CODE):
    session = requests.session()
    r = session.get(URL_BASE, headers=headers)

    # Get the login token
    soup = BeautifulSoup(r.content, "html.parser")
    tokens = {"_token": soup.find_all("input", attrs={"name": "_token"})[0].attrs["value"]}

    # Send login request
    data = {"method": "POST",
            "_token": tokens["_token"],
            "email": NUMBER,
            "password": CODE
            }

    # saveOutput('before', session)  # print(r.url)
    r = session.post(URL_BASE + LOGIN_STUB, data=data, headers=headers)
    # print(r.url) # saveOutput('after', session)

    return session, tokens, data


def saveOutput(save_file_st_end, session):
    page = session.get(URL_BASE + SEND_STUB, verify=False)
    # data = re.findall(r'<h1(.*?)</h1>', str(page.content))
    data = str(page.content)

    if "before" not in str(save_file_st_end):
        to_open = 'after_login.txt'
    else:
        to_open = 'before_login.txt'

    f = open(to_open, 'w+')
    f.write(str(data))
    f.close()


def load_message():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + "message.txt"
    text_file = open(file_path, "r")
    contents = text_file.read()
    text_file.close()
    return contents


def send_message(session, tokens, message, number):
    data = {"message": message,
            "recipients_contacts[]": number + '|contact',
            "scheduled_date": "",
            "scheduled_time": "",
            "inputDatetime": "",
            }
    data.update(tokens)  # Add the tokens

    r = session.post(URL_BASE + SEND_STUB, data=data, headers=headers)


def how_many_left(session):
    r = session.get(URL_BASE + SEND_STUB, verify=False)
    # soup = BeautifulSoup(r.content, "html.parser")
    g_data = re.findall(r'<strong>(.*?)</strong>', str(r.content))

    remaining_texts = g_data[0].split('/')[0]
    print('There are %s remaining texts' % remaining_texts)


def main(sent_to='0871234567', message=None):
    create_user_data()
    NUMBER, CODE = login_data()
    session, tokens, data = login_three(NUMBER, CODE)
    if not message:
        message = load_message()
    send_message(session, tokens, message, sent_to)
    how_many_left(session)

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
URL_BASE = "https://webtexts.three.ie"
LOGIN_STUB = "/users/login"
LOGOUT_STUB = "/users/logout"
SEND_STUB = "/messages/send"




