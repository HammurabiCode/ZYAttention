from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    data = {'tests':[]}
    players = [p.player_id for p in AttApp.models.Player.objects.filter()]
    tests = AttApp.models.Test.objects.all()
    for t in tests:
        t_data = {'date_time': t.date_time.strftime('%Y-%m-%d %H:%M:%S'),
        'scores':[]}
        for sc in AttApp.models.Score.objects.filter(test=t).select_related():
            t_data['scores'].append({'player':sc.player.player_id,
                'score':sc.score})

        data['tests'].append(t_data)

    return render(request, 'index.html', data)

def startTest(request):
    return HttpResponse('true')

import AttApp.models
import json
import datetime

def score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        strtime = data.get('date_time', None)
        scores = data.get('scores', None)
        if strtime and len(scores) > 0:
            date_time = datetime.datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
            print(date_time)
            t = AttApp.models.Test.objects.create(date_time=date_time)
            cnt = 0
            for p_id in scores:
                p = AttApp.models.Player.objects.get(player_id=p_id)
                if not p:
                    continue

                s = AttApp.models.Score.objects.create(player=p, test=t, score=scores[p_id])
                cnt += 1
            pass
            if cnt == 0:
                t.delete()
        else:
            return HttpResponse('No datetime recieved.')
    return HttpResponse('ok')

'''
        strtime = request.POST.get('datetime', None)
        if strtime:
            d = datetime.datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
            t = models.Test(date_time=d)
            t.save()
            frame_dict = {i:int(request.POST.get(str(i))) for i in range(len(request.POST) - 1)}
            for k, v in frame_dict.items():
                models.Frame(test=t, no=k, height=v).save()
'''


def player(request):
    q1=[]
    if request.method == 'POST':
        player_id = request.POST.get('player_id', None)
        if player_id:
            q1 = AttApp.models.Player.objects.filter(player_id=player_id)
            if len(q1) == 0:
                AttApp.models.Player.objects.create(player_id=player_id)
    return HttpResponse('OK')


def history(request):
    history_list = {'data':[]}
    if request.method == 'GET':
        player_id = request.GET.get('player_id', None)
        if player_id:
            q1 = AttApp.models.Score.objects.filter(player_id=player_id).order_by('-test')
            print(len(q1))
            for q in q1:
                h = {}
                h['date_time'] = q.test.date_time.strftime('%m-%d %H:%M:%S')
                h['score'] = q.score
                history_list['data'].append(h)

    return HttpResponse(json.dumps(history_list), content_type='application/json')


def test_lib(request):
    data = {}
    return render(request, 'test_lib.html', data)
