from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# posts = [
#     {
#         'title': 'Journal 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2021'
#     },
#     {
#         'title': 'Journal 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2021'
#     },
#     {
#         'content': 'Third post content',
#         'date_posted': 'August 29, 2021'
#     }
# ]

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def habits(request):
    return render(request, 'app/habits.html')

def journals(request):
    context = {
        'posts': Post.objects.filter(author=request.user).order_by('-date_posted')
    }
    return render(request, 'app/journals.html', context)