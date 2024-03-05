from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Notice, Comment, Choice
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import CommentForm, NoticeForm


def loginView(request):
    if request.user.is_authenticated:
        return render(request, 'secureapp/login.html')
    else:
        return render(request, 'secureapp/login.html')


#@login_required
class homeView(generic.ListView):
    template_name = 'secureapp/home.html'
    context_object_name = 'notice_list'

    def get_queryset(self):
        return Notice.objects.order_by('-pub_date')
    
    #FLAW: CSRF
    #   Without CSRF-protection, it is possible to access data 
    #   as an authenticated user that should not be accessible.
    #   
    #   To fix the flaw, comment lines with @csrf_exempt (lines 36, 84 and 106)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = NoticeForm(request.POST)

        if request.user.is_authenticated:
            print(form)
            if form.is_valid():
                newn = form.save(commit=False)
                newn.save() # new notice added
                choice1 = Choice(notice = newn, choice_text = 'Good notice', votes=0)
                choice1.save()
                choice2 = Choice(notice = newn, choice_text = 'Irrelevant notice', votes=0)
                choice2.save() # added the voting choices
            return self.get(request, *args, **kwargs)
        else:
            messages.error(request, 'Log in to add notice!')
            return redirect('secureapp:login')
        
    def get(self, request, *args, **kwargs):
        notices = Notice.objects.order_by('-pub_date')
        form = NoticeForm()
        return render(request, self.template_name, {'notice_list': notices, 'form': form})


#@login_required
class DetailView(generic.DetailView):
    model = Notice
    template_name = 'secureapp/details.html'
 
    def get(self, request, *args, **kwargs):
        n = self.get_object()
        
        #FLAW: (SQL-)injection 
        #   We can use Djangos built in option to filter data to avoid injection.
        #   Data should be filtered (or validated) before reaching the database to avoid attacker
        #   having access directly to the database.
        #   To fix the flaw, uncomment the line 74 and comment lines 76-79.
        
        #comments = Comment.objects.filter(notice=n)
        
        comments = Comment.objects.all()
        sqlq = request.GET.get('search')
        if sqlq:
            comments = Comment.objects.raw("SELECT * FROM Comment WHERE title LIKE '%{}%'".format(sqlq))
        
        form = CommentForm()
        return render(request, self.template_name, {'notice': n, 'comments': comments, 'form': form})
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        notice = self.get_object()
        form = CommentForm(request.POST)

        if request.user.is_authenticated:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.notice = notice
                new_comment.save()
            return self.get(request, *args, **kwargs)
        else:
            messages.error(request, 'Log in to comment!')
            return redirect('secureapp:login')
  
 
#@login_required
class ResultsView(generic.DetailView):
    model = Notice
    template_name = 'secureapp/results.html'

@csrf_exempt
def vote(request, notice_id):
    nn = get_object_or_404(Notice, pk = notice_id)
    try:
        selected_choice = nn.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'secureapp/details.html',
{
    'notice': nn,
    'error_message': "You didn't select a choice."
})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('secureapp:results', args=(notice_id,)))
    
