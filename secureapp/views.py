from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Notice


def index(request):
    return HttpResponse("the secure app login page")

def homeView(request):
    notice_list = Notice.objects.order_by('-pub_date')
    context = {'notice_list': notice_list}
    return render(request, 'secureapp/home.html', context)
    #return HttpResponse("the secure app")
    
