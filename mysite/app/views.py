from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'app/home.html')

@login_required
def habits(request):
    return render(request, 'app/habits.html')

@login_required
def journals(request):
    context = {
        'posts': Post.objects.filter(author=request.user).order_by('-date_posted')
    }
    return render(request, 'app/journals.html', context)