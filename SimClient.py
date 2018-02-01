import json
import datetime
import random
import requests

host = 'http://127.0.0.1:8080/'

def randomScore():
    return int(random.random()*20)

def addScore():
    data = {
        'date_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'scores': {
            'P01': randomScore(),
            'P02': randomScore(),
            'P03': randomScore(),
            'P04': randomScore(),
            'P05': randomScore(),
            'P06': randomScore(),
            'P07': randomScore()
            },
        }
    resp = requests.post(host+'score', json=data)
    print(resp)


def genPlayer():
    for i in range(10):
        yield 'P{:0>2}'.format(i),


def addPlayer(player_id):
    data = {
        'player_id': player_id
    }
    resp = requests.post(host+'player', data=data)


if __name__ == '__main__':
    addScore()
    pass
    # main()