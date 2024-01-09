from django.shortcuts import render
from .models import Post, Habit, DailyPerformance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def home(request):
    return render(request, 'app/home.html')


######### JOURNAL VIEWS #########

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


######### HABIT VIEWS #########

@login_required
def habits(request):
    return render(request, 'app/habits.html')

# TODO: initialize DailyPerformance records when a new week starts.
@login_required
def week_reset(request):
    """Reset all habits for the week."""
    # redirect to habits page
    return render(request, 'app/habits.html')


# TODO: initialize DailyPerformance records when a new habit is created.
class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    template_name = 'app/habit_create.html'
    fields = ['title', 'goal']
    success_url = '/habits/'

    def form_valid(self, form):
        """Override to set the user of the new habit to the logged-in user."""
        form.instance.user = self.request.user
        resp = super().form_valid(form)
        messages.success(self.request, f'Habit created!')
        return resp


class HabitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Habit
    template_name = 'app/habit_update.html'
    fields = ['title', 'goal']
    success_url = '/habits/'

    def form_valid(self, form):
        """Override to set the user of the new habit to the logged-in user."""
        form.instance.user = self.request.user
        resp = super().form_valid(form)
        messages.success(self.request, f'Habit updated!')
        return resp

    def test_func(self):
        """Override to restrict editing to the author of the habit."""
        habit = self.get_object()
        return self.request.user == habit.user


class HabitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Habit
    template_name = 'app/habit_confirm_delete.html'
    success_url = '/habits/'

    def test_func(self):
        """Override to restrict editing to the author of the habit."""
        habit = self.get_object()
        return self.request.user == habit.user
