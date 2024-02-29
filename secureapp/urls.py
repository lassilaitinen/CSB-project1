from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'secureapp'
urlpatterns = [
    path('home', views.homeView.as_view(), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:notice_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
]