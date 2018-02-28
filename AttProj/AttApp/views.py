from django.shortcuts import render
from django.shortcuts import HttpResponse
import AttApp.models
import json
import datetime
import random


cur_quiz_id = 0


# Create your views here.
def index(request):
    data = {}
    data['student_list'] = [stu.stu_no for stu in AttApp.models.Student.objects.all()]
    data['student_cnt'] = len(AttApp.models.Student.objects.all())
    data['test_cnt'] = len(AttApp.models.Test.objects.all())
    data['quiz_cnt'] = len(AttApp.models.Quiz.objects.all())
    data['quiz_test_cnt'] = len(AttApp.models.QuizTest.objects.all())
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
        test_data = json.loads(str_json)
        t = AttApp.models.Test.objects.create(date_time=datetime.datetime.now)
        cnt = 0
        try:
            for dev_no in test_data:
                dev = AttApp.models.Device.objects.get(dev_no=dev_no)
                stu = AttApp.models.StuDevMap.objects.get(dev=dev).stu
                react_data = {
                    'stu':stu,
                    'test':t,
                    'score': test_data[dev_no],
                    'dev': dev
                }
                react = AttApp.models.ReactionTime.objects.create(**react_data)
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
    for sc in AttApp.models.ReactionTime.objects.filter(test=test).select_related()[0:4]:
        data['records'].append({'stu':sc.stu.stu_no, 'score':sc.score})
    return render(request, 'zhy/test_detail.html', data)



def quiz(request):
    if request.method == 'GET':
        data = {'quiz_list':[]}
        quiz_list = AttApp.models.Quiz.objects.order_by('quiz_id')
        for q in quiz_list:
            q_rec = {'title': q.title,
                'options': {chr(idx+ord('A')): opt for idx, opt in enumerate(q.getOptions())},
                'answer': chr(q.answer+ord('A'))
            }
            data['quiz_list'].append(q_rec)
        data['quiz_cnt'] = len(data['quiz_list'])
        return render(request, 'zhy/quiz.html', data)
    if request.method == 'POST':
        str_json = str(request.body.decode('utf-8'))
        quiz= json.loads(str_json)
        title = quiz.get('title', None)
        answer = quiz.get('answer', None)
        options = quiz.get('options', None)

        if title and answer and options:
            try:
                q = AttApp.models.Quiz.objects.create(title=title, answer=answer, options_str='\n'.join(options))
                return HttpResponse('Quiz added!')
            except Exception as e:
                return HttpResponse(str(e))
            else:
                pass
            finally:
                pass
    return HttpResponse('No quiz added!')


def quiz_test(request):
    if request.method == 'GET':
        data = {'quiz_tests':[]}
        quiz_tests = AttApp.models.QuizTest.objects.order_by('-date_time')
        for sc in quiz_tests:
            qt = {
                'date_time':sc.date_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            data['quiz_tests'].append(qt)
        data['quiz_test_cnt'] = len(data['quiz_tests'])
        return render(request, 'zhy/quiz_test.html', data)
    elif request.method == 'POST':
        str_json = str(request.body.decode('utf-8'))
        scores = json.loads(str_json)
        print(cur_quiz_id)
        quiz_test_data = {
            'date_time': datetime.datetime.now,
            'quiz': AttApp.models.Quiz.objects.get(quiz_id=cur_quiz_id)
        }
        qt = AttApp.models.QuizTest.objects.create(**quiz_test_data)
        cnt = 0
        try:
            for dev_no in scores:
                dev = AttApp.models.Device.objects.get(dev_no=dev_no)
                stu = AttApp.models.StuDevMap.objects.get(dev=dev).stu
                quiz_data = {
                    'stu':stu,
                    'quiz_test':qt,
                    'choice': ord(scores[dev_no]['answer'])-ord('A'), 
                    'time': scores[dev_no]['time'],
                    'dev': dev
                }
                AttApp.models.QuizAnswer.objects.create(**quiz_data)
                cnt += 1
        except Exception as e:
            qt.delete()
            return HttpResponse(str(e))
        else:
            qt.save()
        finally:
            pass
        if cnt == 0:
            qt.delete()
            return HttpResponse('No student')
        else:
            qt.save()
    return HttpResponse('test added!')
    pass

def quiz_test_detail(request):
    quiz_test = None
    str_date_time = request.GET.get('date_time')
    if str_date_time:
        date_time=datetime.datetime.strptime(str_date_time, '%Y-%m-%d %H:%M:%S')
        qs = AttApp.models.QuizTest.objects.filter(date_time__year=date_time.year, 
            date_time__month=date_time.month, date_time__day=date_time.day,
            date_time__hour=date_time.hour, date_time__minute=date_time.minute,
            date_time__second=date_time.second)
        if len(qs) != 1:
            return HttpResponse('Error datetime: {}'.format(str_date_time))
        else:
            quiz_test = qs[0]

        data = {
            'date_time': date_time,
            'quiz' : 
                {
                    'title': quiz_test.quiz.title,
                    'options': {chr(idx+ord('A')): opt for idx, opt in enumerate(quiz_test.quiz.getOptions())},
                    'answer': chr(quiz_test.quiz.answer+ord('A'))
                },
            'answers' :[]
        }
        answers = AttApp.models.QuizAnswer.objects.filter(quiz_test=quiz_test)
        for a in answers:
            answer_data = {
                'stu_no': a.stu.stu_no,
                'choice': chr(a.choice+ord('A')),
                'time': a.time
            }
            data['answers'].append(answer_data)
        print(data['answers'])

        return render(request, 'zhy/quiz_test_detail.html', data)


def player(request):
    q1=[]
    str_resp = ''
    if request.method == 'POST':
        stu_no = request.POST.get('stu_no', None)
        if stu_no:
            q1 = AttApp.models.Student.objects.filter(stu_no=stu_no)
            if len(q1) == 0:
                AttApp.models.Student.objects.create(stu_no=stu_no)
    elif request.method == 'GET':
        player_list = AttApp.models.Student.objects.all()
        str_resp = '{}\n{}'.format(str_resp, len(player_list))
        for p in player_list:
            str_resp = '{}\n{}'.format(str_resp, p.stu_no)
    return HttpResponse(str_resp)


def history(request):
    history_list = {'data':[]}
    if request.method == 'GET':
        stu_no = request.GET.get('stu_no', None)
        if stu_no:
            q1 = AttApp.models.ReactionTime.objects.filter(stu_no=stu_no).order_by('-test')
            for q in q1:
                h = {}
                h['date_time'] = q.test.date_time.strftime('%m-%d %H:%M:%S')
                h['score'] = q.score
                history_list['data'].append(h)

    return HttpResponse(json.dumps(history_list), content_type='application/json')

def clear_db(request):
    for p in AttApp.models.Student.objects.all():
        p.delete()
    for t in AttApp.models.StuDevMap.objects.all():
        t.delete()
    for t in AttApp.models.Device.objects.all():
        t.delete()
    for t in AttApp.models.QuizTest.objects.all():
        t.delete()
    for t in AttApp.models.Test.objects.all():
        t.delete()
    for t in AttApp.models.Quiz.objects.all():
        t.delete()
    return HttpResponse('ok')

def init_db(request):
    clear_db(request)
    # 学生
    name_list = {
        '1801': '赵一',
        '1802': '王二',
        '1803': '张三',
        '1804': '李四'
    }
    for stu_no in name_list:
        AttApp.models.Student.objects.create(stu_no=stu_no, name=name_list[stu_no])

    device_stu_no = {
        '1': '1801',
        '2': '1802',
        '3': '1803',
        '4': '1804'
    }
    # 设备，设备学生的映射关系
    for dev_no in device_stu_no:
        dev = AttApp.models.Device.objects.create(dev_no=dev_no)
        stu_no = device_stu_no[dev_no]
        stu = AttApp.models.Student.objects.filter(stu_no=stu_no)
        if len(stu) == 1:
            AttApp.models.StuDevMap.objects.create(stu=stu[0],dev=dev)

    # 题目
    quiz_data = {
        'title' : '导电性最好的金属是?',
        'options_str' : '\n'.join(['金', '银', '铜', '铁']),
        'answer' : 1

    }
    quiz = AttApp.models.Quiz.objects.create(**quiz_data)
    global cur_quiz_id
    cur_quiz_id = quiz.quiz_id
    print(cur_quiz_id)

    # 反应力测试
    test = AttApp.models.Test.objects.create(date_time=datetime.datetime.now)
    for dev_no in device_stu_no:
        dev = AttApp.models.Device.objects.get(dev_no=dev_no)
        stu = AttApp.models.StuDevMap.objects.get(dev=dev).stu
        react = AttApp.models.ReactionTime.objects.create(stu=stu, test=test, score=int(random.random()*20), dev=dev)

    # 问答测试
    quiz_test = AttApp.models.QuizTest.objects.create(quiz=quiz, date_time=datetime.datetime.now)
    for dev_no in device_stu_no:
        dev = AttApp.models.Device.objects.get(dev_no=dev_no)
        stu = AttApp.models.StuDevMap.objects.get(dev=dev).stu
        data = {
            'stu':stu,
            'quiz_test':quiz_test,
            'choice': int(random.random()*4),
            'time': int(random.random()*20),
            'dev': dev
        }
        AttApp.models.QuizAnswer.objects.create(**data)


    return index(request)


def test_lib(request):
    data = {}
    return render(request, 'test_lib.html', data)
