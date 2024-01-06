from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

def home(request):
    return render(request, 'app/home.html')

@login_required
def habits(request):
    return render(request, 'app/habits.html')

# @login_required
# def journals(request):
#     context = {
#         'posts': Post.objects.filter(author=request.user).order_by('-date_posted')
#     }
#     return render(request, 'app/journals.html', context)

class JournalListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'app/journals.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Override to get posts only by the logged-in user."""
        user = self.request.user
        return Post.objects.filter(author=user).order_by('-date_posted')

class JournalDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'app/journal_detail.html'
    context_object_name = 'post'