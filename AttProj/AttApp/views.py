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
    '1': 'S01',
    '2': 'S02',
    '3': 'S03',
    '4': 'S04'
}


# Create your views here.
def index(request):
    data = {}
    data['student_list'] = [p.player_id for p in AttApp.models.Player.objects.all()]
    data['student_cnt'] = len(AttApp.models.Player.objects.all())
    data['test_cnt'] = len(AttApp.models.Test.objects.all())
    data['quiz_cnt'] = len(AttApp.models.Quiz.objects.all())
    return render(request, 'zhy/index.html', data)

def test(request):
    if request.method == 'GET':
        data = {'tests':[]}
        tests = AttApp.models.Test.objects.order_by('-date_time')
        for sc in tests:
            data['tests'].append(sc.date_time.strftime('%Y-%m-%d %H:%M:%S'))
        data['test_cnt'] = len(data['tests'])
        return render(request, 'zhy/test.html', data)
    elif request.method == 'POST':
        str_json = str(request.body.decode('utf-8'))
        scores = json.loads(str_json)
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
            return HttpResponse(str(e))
        else:
            t.save()
        finally:
            pass
        if cnt == 0:
            t.delete()
            return HttpResponse('No student')
        else:
            t.save()
    return HttpResponse('test added!')


def test_detail(request):
    test = None
    str_date_time = request.GET.get('date_time')
    if str_date_time:
        date_time=datetime.datetime.strptime(str_date_time, '%Y-%m-%d %H:%M:%S')
        qs = AttApp.models.Test.objects.filter(date_time__year=date_time.year, 
            date_time__month=date_time.month, date_time__day=date_time.day,
            date_time__hour=date_time.hour, date_time__minute=date_time.minute,
            date_time__second=date_time.second)
        if len(qs) != 1:
            return HttpResponse('Error datetime: {}'.format(str_date_time))
        else:
            test = qs[0]
    else:
        return HttpResponse('Please input date time.')

    data = {'records':[], 'test_date_time':str_date_time}
    for sc in AttApp.models.ReactionScore.objects.filter(test=test).select_related()[0:4]:
        data['records'].append({'player':sc.player.player_id, 'score':sc.score})
    return render(request, 'zhy/test_detail.html', data)


def score(request):
    str_json = str(request.body.decode('utf-8'))
    if request.method == 'POST':
        scores = json.loads(str_json)
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
            return HttpResponse(str(e))
        else:
            t.save()
        finally:
            pass
        if cnt == 0:
            t.delete()
            return HttpResponse('No student')
        else:
            t.save()
    return HttpResponse('ok')


def player(request):
    q1=[]
    str_resp = ''
    if request.method == 'POST':
        player_id = request.POST.get('player_id', None)
        if player_id:
            q1 = AttApp.models.Player.objects.filter(player_id=player_id)
            if len(q1) == 0:
                AttApp.models.Player.objects.create(player_id=player_id)
    elif request.method == 'GET':
        player_list = AttApp.models.Player.objects.all()
        str_resp = '{}\n{}'.format(str_resp, len(player_list))
        for p in player_list:
            str_resp = '{}\n{}'.format(str_resp, p.player_id)
    return HttpResponse(str_resp)


def history(request):
    history_list = {'data':[]}
    if request.method == 'GET':
        player_id = request.GET.get('player_id', None)
        if player_id:
            q1 = AttApp.models.ReactionScore.objects.filter(player_id=player_id).order_by('-test')
            for q in q1:
                h = {}
                h['date_time'] = q.test.date_time.strftime('%m-%d %H:%M:%S')
                h['score'] = q.score
                history_list['data'].append(h)

    return HttpResponse(json.dumps(history_list), content_type='application/json')

def clear_db(request):
    for p in AttApp.models.Player.objects.all():
        p.delete()
    for t in AttApp.models.Test.objects.all():
        t.delete()
    return HttpResponse('ok')

def init_db(request):
    for dev in device_stu_no:
        player_id = device_stu_no[dev]
        if 0 == len(AttApp.models.Player.objects.filter(player_id=player_id)):
            AttApp.models.Player.objects.create(player_id=player_id)
    return HttpResponse('ok')


def test_lib(request):
    data = {}
    return render(request, 'test_lib.html', data)
