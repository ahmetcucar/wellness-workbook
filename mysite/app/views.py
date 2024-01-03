from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'title': 'Journal 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2021'
    },
    {
        'title': 'Journal 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2021'
    },
    {
        'content': 'Third post content',
        'date_posted': 'August 29, 2021'
    }
]

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def habits(request):
    return render(request, 'app/habits.html')

def journals(request):
    return render(request, 'app/journals.html', {'posts': posts})