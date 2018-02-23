import json
import datetime
import random
import requests

host = 'http://127.0.0.1:8080/'
ali_host = 'http://106.14.196.64:8081/'

def randomScore():
    return int(random.random()*20)

def addScore():
    data = {
        '1': randomScore(),
        '2': randomScore(),
        '3': randomScore(),
        '4': randomScore()
    }
    headers = {'Content-type': 'application/json'}
    # resp = requests.post(host+'score/', json=data, headers=headers)
    resp = requests.post(ali_host+'score/', json=data, headers=headers)
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
    addScore()
    # test()
