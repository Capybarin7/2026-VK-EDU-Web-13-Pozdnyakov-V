from django.contrib import admin
from questions.models import Profile, Question, Answer, Tag, QuestionTag, AnswerLike, QuestionLike
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1
    verbose_name_plural = "Ответы"
    raw_id_fields = ("author",)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    raw_id_fields = ("user",)
    search_fields = ("user__username",)
    list_filter = ("user__is_active",)
    list_select_related = ("user",)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "createdAt")
    raw_id_fields = ("author",)
    search_fields = ("name", "text")
    list_filter = ("author", "createdAt")
    inlines = (AnswerInline,)
    list_select_related = ("author",)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "author", "createdAt", "isRight")
    raw_id_fields = ("question", "author")
    search_fields = ("text",)
    list_filter = ("isRight", "author", "createdAt")
    list_select_related = ("question", "author")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)

@admin.register(QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "tag")
    raw_id_fields = ("question","tag")
    search_fields = ("question__name", "tag__name")
    list_filter = ("tag__name",)
    list_select_related = ("question", "tag")

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "answer", "author")
    raw_id_fields = ("answer", "author")
    search_fields = ("answer__text", "author__user__username")
    list_filter = ("author",)
    list_select_related = ("answer", "author")


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "author")
    raw_id_fields = ("question", "author")
    search_fields = ("question__name", "author__user__username")
    list_filter = ("author",)
    list_select_related = ("question", "author")
