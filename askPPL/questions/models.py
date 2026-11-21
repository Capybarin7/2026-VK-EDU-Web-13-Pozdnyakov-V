from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os
import uuid
# Create your models here.

def avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)
    return f"images/{uuid.uuid4()}{ext}"

class QuestionManager(models.Manager):
    def latest(self):
        return self.order_by('-createdAt').annotate(answers_count=models.Count('answers', distinct=True), likes_count=models.Count('question_like', distinct=True))

    def popular(self):
        return self.annotate(answers_count=models.Count('answers', distinct=True), likes_count=models.Count('question_like', distinct=True)).order_by('-likes_count')

    def with_tag(self, tag_name):
        return self.filter(tags__name=tag_name).annotate(answers_count=models.Count('answers', distinct=True), likes_count=models.Count('question_like', distinct=True))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ник")
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True, default='images/default.png', verbose_name="Аватар")
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    def __str__(self):
        return f"Профиль {self.user.username}"

class Tag(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название тега")
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.TextField(max_length=300, verbose_name="Описание")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор")
    tags = models.ManyToManyField(Tag, through='QuestionTag', verbose_name="Теги")
    objects = QuestionManager()
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('question_detail', args=[self.id])
    def has_like(self, user: User):
        from questions.models import QuestionLike
        if not user.is_authenticated: return False
        return QuestionLike.objects.filter(question=self, author = user.profile).exists()


class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")
    class Meta:
        verbose_name = "Связь вопроса с тегом"
        verbose_name_plural = "Связи вопросов с тегами"
    def __str__(self):
        return f"{self.question.name} - {self.tag.name}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос", related_name='answers')
    text = models.TextField(max_length=300, verbose_name="Текст ответа")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор")
    isRight = models.BooleanField(default=False, verbose_name="Правильный ответ")
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
    def __str__(self):
        return f"Ответ #{self.id} от {self.author.user.username}"
    def likes_count(self):
        return self.answer_like.count()
    def has_like(self, user: User):
        from questions.models import AnswerLike
        if not user.is_authenticated: return False
        return AnswerLike.objects.filter(answer=self, author = user.profile).exists()

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос", related_name='question_like')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор лайка")
    class Meta:
        unique_together = ('question', 'author')
        verbose_name = "Лайк вопроса"
        verbose_name_plural = "Лайки вопроса"
    def __str__(self):
        return f"Лайк {self.author.user.username} -> {self.question.name}"

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Ответ", related_name='answer_like')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Автор лайка")
    class Meta:
        unique_together = ('answer', 'author')
        verbose_name = "Лайк ответа"
        verbose_name_plural = "Лайки ответа"
    def __str__(self):
        return f"Лайк {self.author.user.username} -> ответ #{self.answer.id}"


