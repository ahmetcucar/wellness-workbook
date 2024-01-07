from django.shortcuts import render
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def home(request):
    return render(request, 'app/home.html')

@login_required
def habits(request):
    return render(request, 'app/habits.html')


class JournalListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'app/journal.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Override to get posts only by the logged-in user."""
        user = self.request.user
        return Post.objects.filter(author=user).order_by('-date_posted')


class JournalDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'app/journal_detail.html'
    context_object_name = 'post'


class JournalCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'app/journal_create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        """Override to set the author of the new post to the logged-in user."""
        form.instance.author = self.request.user
        resp = super().form_valid(form)
        messages.success(self.request, f'Journal entry created!')
        return resp


class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'app/journal_update.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        """Override to set the author of the new post to the logged-in user."""
        form.instance.author = self.request.user
        resp = super().form_valid(form)
        messages.success(self.request, f'Journal entry updated!')
        return resp

    def test_func(self):
        """Override to restrict editing to the author of the post."""
        post = self.get_object()
        return self.request.user == post.author


class JournalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'app/journal_confirm_delete.html'
    success_url = '/journals/'

    def test_func(self):
        """Override to restrict editing to the author of the post."""
        post = self.get_object()
        return self.request.user == post.author