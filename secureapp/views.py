from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Notice, Comment, Choice
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CommentForm


def loginView(request):
    if request.user.is_authenticated:
        return render(request, 'secureapp/login.html')
    else:
        return render(request, 'secureapp/login.html')
    #return HttpResponse("the secure app login page")


#@login_required
class homeView(generic.ListView):
#def homeView(request):
    template_name = 'secureapp/home.html'
    context_object_name = 'notice_list'

    def get_queryset(self):
        return Notice.objects.order_by('-pub_date')

#@login_required
class DetailView(generic.DetailView):
    model = Notice
    template_name = 'secureapp/details.html'
 
    def get(self, request, *args, **kwargs):
        n = self.get_object()
        comments = Comment.objects.all()
        sqlq = request.GET.get('search')
        if sqlq:
            comments = Comment.objects.raw("SELECT * FROM Comment WHERE title LIKE '%{}%'".format(sqlq))
        form = CommentForm()
        return render(request, self.template_name, {'notice': n, 'comments': comments, 'form': form})
    
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
        #return redirect('secureapp:detail', pk = notice.pk)
    
#@login_required
class ResultsView(generic.DetailView):
    model = Notice
    template_name = 'secureapp/results.html'

#@login_required
def add_comment(request):
    if request.method == 'POST':
        commenttext = request.POST('commenttext')
        #if request.user.is_authenticated:
        new_comment = Comment.objects.create(user=request.user, comment_text=commenttext)
            #messages.success(request, 'Comment sent.')
        return render(request, 'secureapp/details.html', {'comment': new_comment})
        #else:
        #    messages.error(request, 'Log in to comment!')
        #    return redirect('secureapp:login')

    else:
        return render(request, 'secureapp/add_comment.html')
    
    
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
