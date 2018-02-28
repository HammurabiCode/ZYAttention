import json
import datetime
import random
import requests

host = 'http://127.0.0.1:8080/'
ali_host = 'http://106.14.196.64:8081/'

def randomScore():
    return int(random.random()*20)

def postTest():
    data = {
        '1': randomScore(),
        '2': randomScore(),
        '3': randomScore(),
        '4': randomScore()
    }
    headers = {'Content-type': 'application/json'}
    resp = requests.post(host+'test/', json=data, headers=headers)
    # resp = requests.post(ali_host+'test/', json=data, headers=headers)
    print(resp.text)
    with open('resp.html', 'w') as pf:
        pf.write(resp.text)

def postQuiz():
    data = {
        'title':'导电性最好的金属是?',
        'options':['金', '银', '铜', '铁'],
        'answer':1
    }
    headers = {'Content-type': 'application/json'}
    resp = requests.post(host+'quiz/', json=data, headers=headers)
    # resp = requests.post(ali_host+'quiz/', json=data, headers=headers)
    print(resp.text)
    pass


def postQuizTest():
    data = {
        '1': {'time':randomScore(), 'answer':'A'},
        '2': {'time':randomScore(), 'answer':'B'},
        '3': {'time':randomScore(), 'answer':'C'},
        '4': {'time':randomScore(), 'answer':'D'},
    }
    print(data)
    headers = {'Content-type': 'application/json'}
    # resp = requests.post(host+'quiz_test/', json=data, headers=headers)
    resp = requests.post(ali_host+'quiz_test/', json=data, headers=headers)
    print(resp.text)
    with open('resp.html', 'w') as pf:
        pf.write(resp.text)


def genPlayer():
    for i in range(10):
        yield 'P{:0>2}'.format(i),


def addPlayer(player_id):
    data = {
        'player_id': player_id
    }
    resp = requests.post(host+'player', data=data)

def test():
    data = {
        '1': randomScore(),
        '2': randomScore(),
        '3': randomScore(),
        '4': randomScore()
    }
    print(data)
    headers = {'Content-type': 'application/json'}
    resp = requests.post(ali_host+'starttest/', json=data, headers=headers)
    with open('resp.html', 'w') as pf:
        pf.write(resp.text)
    print(resp)

if __name__ == '__main__':
    # postQuiz()
    postTest()
    # postQuizTest()
    # test()
