from django.shortcuts import render
from django.http import HttpResponse
from questions.utils.paginationfunc import paginate
from django.http import Http404
# Create your views here.

QUESTION_LIST = [
    {
        'id': i,
        'title': f'Title {i}',
        'text': f'Text {i}' * 10,
        'tags': ['python', 'django'] if i%2 == 0 else ['js', 'go'],
        'answers_count': (i*i)%10,
        'rating': (i*4-i)%10-5,
    } for i in range(30)
]

def index(request):
    page_obj = paginate(QUESTION_LIST, request, per_page=5)
    return render(request, 'questions/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    hot_questions = QUESTION_LIST[::3]
    page_obj = paginate(hot_questions, request, per_page=5)
    return render(request, 'questions/hot.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})


def tag(request, tag_name):
    hotquestions = [q for q in QUESTION_LIST if tag_name in q.get('tags', [])]
    page_obj = paginate(hotquestions, request, per_page=5)
    return render(request, 'questions/tag.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name})

def question_detail(request, question_id):
    for q in QUESTION_LIST:
        if q['id'] == question_id:
            question = q
            break
    else: raise Http404("Вопрос не найден")
    answers = [
        {
            'id': i,
            'text': f'Ответ {i} на вопрос "{question["title"]}"',
            'is_correct': i % 3 == 0,
            'rating': (i*4-i)%10-5,
        } for i in range(question['answers_count'])
    ]
    page_obj = paginate(answers, request, per_page=5)
    return render(request, 'questions/question_detail.html', context={ 'question': question, 'page_obj': page_obj})

def ask(request):
    return render(request, 'questions/ask.html')