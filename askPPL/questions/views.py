from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from questions.forms import AnswerForm
from questions.utils.paginationfunc import paginate
from django.http import Http404
from questions.models import Question, Answer, QuestionLike, AnswerLike
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import AskForm, AnswerForm
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    questions = Question.objects.latest().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=5)
    liked_q = list(QuestionLike.objects.filter(author=request.user.profile).values_list('question_id', flat=True)) if request.user.is_authenticated else []
    liked_a = list(AnswerLike.objects.filter(author=request.user.profile).values_list('answer_id', flat=True)) if request.user.is_authenticated else []
    return render(request, 'questions/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'liked_q': liked_q, 'liked_a': liked_a})

def hot(request):
    questions = Question.objects.popular().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=5)
    liked_q = list(QuestionLike.objects.filter(author=request.user.profile).values_list('question_id', flat=True)) if request.user.is_authenticated else []
    liked_a = list(AnswerLike.objects.filter(author=request.user.profile).values_list('answer_id', flat=True)) if request.user.is_authenticated else []
    return render(request, 'questions/hot.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'liked_q': liked_q, 'liked_a': liked_a})


def tag(request, tag_name):
    questions = Question.objects.with_tag(tag_name).select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=5)
    liked_q = list(QuestionLike.objects.filter(author=request.user.profile).values_list('question_id', flat=True)) if request.user.is_authenticated else []
    liked_a = list(AnswerLike.objects.filter(author=request.user.profile).values_list('answer_id', flat=True)) if request.user.is_authenticated else []
    return render(request, 'questions/tag.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name, 'liked_q': liked_q, 'liked_a': liked_a})

def question_detail(request, question_id):
    question = get_object_or_404(Question.objects.annotate(likes_count=Count('question_like', distinct = True), answers_count=Count('answers', distinct = True)), id=question_id)
    answers = question.answers.select_related('author').order_by("-createdAt")
    page_obj = paginate(answers, request, per_page=3)
    liked_q = list(QuestionLike.objects.filter(author=request.user.profile).values_list('question_id', flat=True)) if request.user.is_authenticated else []
    liked_a = list(AnswerLike.objects.filter(author=request.user.profile).values_list('answer_id', flat=True)) if request.user.is_authenticated else []
    if request.method == 'POST':
        form = AnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            return redirect(f'/question/{question.id}/#answer_{answer.id}')
    else:
        form = AnswerForm(user=request.user, question=question)
    return render(request, 'questions/question_detail.html', context={ 'question': question, 'page_obj': page_obj, 'form': form, 'liked_q': liked_q, 'liked_a': liked_a})

@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST, user=request.user)
        if form.is_valid():
            question = form.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AskForm(user=request.user)
    return render(request, 'questions/ask.html', {'form': form})

@require_POST
def toggle_correct(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user.profile != answer.question.author:
        return JsonResponse({'is_right': answer.isRight}, status=403)
    answer.isRight = not answer.isRight
    answer.save()
    return JsonResponse({'is_right': answer.isRight})

@require_POST
def like_question(request, question_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    question = get_object_or_404(Question, id=question_id)
    QuestionLike.objects.get_or_create(question=question, author=request.user.profile)
    return JsonResponse({'likes_count': question.question_like.count(), 'status': 'success'})

@require_POST
def unlike_question(request, question_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    question = get_object_or_404(Question, id=question_id)
    QuestionLike.objects.filter(question=question, author=request.user.profile).delete()
    return JsonResponse({'likes_count': question.question_like.count(), 'status': 'success'})

@require_POST
def like_answer(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    answer = get_object_or_404(Answer, id=answer_id)
    AnswerLike.objects.get_or_create(answer=answer, author=request.user.profile)
    return JsonResponse({'likes_count': answer.answer_like.count(), 'status': 'success'})

@require_POST
def unlike_answer(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    answer = get_object_or_404(Answer, id=answer_id)
    AnswerLike.objects.filter(answer=answer, author=request.user.profile).delete()
    return JsonResponse({'likes_count': answer.answer_like.count(), 'status': 'success'})
