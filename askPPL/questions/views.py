from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from questions.utils.paginationfunc import paginate
from django.http import Http404
from questions.models import Question, Answer
# Create your views here.

def index(request):
    questions = Question.objects.latest().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'questions/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    questions = Question.objects.popular().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'questions/hot.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})


def tag(request, tag_name):
    questions = Question.objects.with_tag(tag_name).select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'questions/tag.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name})

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.select_related('author').order_by("-createdAt")
    page_obj = paginate(answers, request, per_page=3)
    return render(request, 'questions/question_detail.html', context={ 'question': question, 'page_obj': page_obj})

def ask(request):
    return render(request, 'questions/ask.html')