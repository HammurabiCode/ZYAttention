from django.shortcuts import render
from django.shortcuts import HttpResponse
import AttApp.models
import json
import datetime

    
# Create your views here.
def index(request):
    test = None
    str_date_time = request.GET.get('date_time')
    # test = AttApp.models.Test.objects.order_by('-date_time')
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
        test = AttApp.models.Test.objects.order_by('-date_time')[0]
        str_date_time=test.date_time.strftime('%Y-%m-%d %H:%M:%S')

    data = {'records':[], 'test_date_time':str_date_time}
    for sc in AttApp.models.ReactionScore.objects.filter(test=test).select_related()[0:4]:
        data['records'].append({'player':sc.player.player_id, 'score':sc.score})
    return render(request, 'zhy_score.html', data)


def history(request):
    data = {'tests':[]}
    tests = AttApp.models.Test.objects.order_by('-date_time')
    for sc in tests:
        data['tests'].append(sc.date_time.strftime('%Y-%m-%d %H:%M:%S'))
    # for t in tests:
    #     t_data = {'date_time': t.date_time.strftime('%Y-%m-%d %H:%M:%S'), 'scores':[]}
    #     for sc in AttApp.models.ReactionScore.objects.filter(test=t).select_related():
    #         t_data['scores'].append({'player':sc.player.player_id, 'score':sc.score})

    #     data['tests'].append(t_data)
    return render(request, 'history.html', data)
