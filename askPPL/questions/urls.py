from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask, name='ask'),
    path('answer/<int:answer_id>/toggle-correct/', views.toggle_correct, name='toggle_correct'),
    path('question/<int:question_id>/like/', views.like_question, name='like_question'),
    path('question/<int:question_id>/unlike/', views.unlike_question, name='unlike_question'),
    path('answer/<int:answer_id>/like/', views.like_answer, name='like_answer'),
    path('answer/<int:answer_id>/unlike/', views.unlike_answer, name='unlike_answer'),
]