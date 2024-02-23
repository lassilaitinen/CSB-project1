from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'secureapp'
urlpatterns = [
    #path('login/', views.CustomLoginView.as_view(), name='login'),
    #path('', views.loginView, name='login'),
    #path('', auth_views.LoginView.as_view(template_name='secureapp/login.html'), name='login'),
    path('home', views.homeView.as_view(), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:notice_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:notice_id>/edit/', views.edit, name='edit'),
    path('<int:notice_id>/addcomment/', views.add_comment, name='add_comment'),
    #path('addnotice/', views.addNotice, name='add'),
]