from django.shortcuts import render
from django.shortcuts import HttpResponse
import AttApp.models
import json
import datetime

name_list = {
    '1': '赵一',
    '2': '王二',
    '3': '张三',
    '4': '李四'
}

device_stu_no = {
    '1': 'P01',
    '2': 'P02',
    '3': 'P03',
    '4': 'P04'
}


# Create your views here.
def index(request):
    data = {'tests':[]}
    players = [p.player_id for p in AttApp.models.Player.objects.filter()]
    tests = AttApp.models.Test.objects.all()
    for t in tests:
        t_data = {'date_time': t.date_time.strftime('%Y-%m-%d %H:%M:%S'),
        'scores':[]}
        for sc in AttApp.models.ReactionScore.objects.filter(test=t).select_related():
            t_data['scores'].append({'player':sc.player.player_id,
                'score':sc.score})

        data['tests'].append(t_data)

    return render(request, 'index.html', data)

def startTest(request):
    return HttpResponse('true')


def score(request):
    if request.method == 'POST':
        scores = json.loads(request.body)
        t = AttApp.models.Test.objects.create(date_time=datetime.datetime.now)
        cnt = 0
        try:
            for p_id in scores:
                p = AttApp.models.Player.objects.get(player_id=device_stu_no[p_id])
                if not p:
                    continue
                s = AttApp.models.ReactionScore.objects.create(player=p, test=t, score=scores[p_id])
                cnt += 1
        except Exception as e:
            t.delete()
            return HttpResponse('No datetime recieved.')
        else:
            t.save()
        finally:
            pass
        if cnt == 0:
            t.delete()
            return HttpResponse('No datetime recieved.')
        else:
            t.save()
    return HttpResponse('ok')


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
            q1 = AttApp.models.ReactionScore.objects.filter(player_id=player_id).order_by('-test')
            # print(len(q1))
            for q in q1:
                h = {}
                h['date_time'] = q.test.date_time.strftime('%m-%d %H:%M:%S')
                h['score'] = q.score
                history_list['data'].append(h)

    return HttpResponse(json.dumps(history_list), content_type='application/json')


def test_lib(request):
    data = {}
    return render(request, 'test_lib.html', data)
