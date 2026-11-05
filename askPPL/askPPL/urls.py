"""
URL configuration for askPPL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from questions import views as q_views
from core import views as c_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', q_views.index, name='index'),
    path('hot/', q_views.hot, name='hot'),
    path('tag/<str:tag_name>/', q_views.tag, name='tag'),
    path('question/<int:question_id>/', q_views.question_detail, name='question_detail'),
    path('ask/', q_views.ask, name='ask'),
    path('profile/', c_views.profile, name='profile'),
    path('login/', c_views.login, name='login'),
    path('signup/', c_views.signup, name='signup'),
]

