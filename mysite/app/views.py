from django.utils import timezone
from django.shortcuts import render
from .models import Post, Habit, DailyPerformance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def home(request):
    return render(request, 'app/home.html')


######### JOURNAL VIEWS #######################################################

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


######### HABIT VIEWS #######################################################

@login_required
def habits(request):
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)
    days_of_week = [start_of_week + timezone.timedelta(days=i) for i in range(7)] # date objects

    habits = Habit.objects.filter(user=request.user)
    habit_data = []
    for habit in habits:
        habit_info = {
            'id': habit.id,
            'title': habit.title,
            'goal': habit.goal,
            'count': habit.count_this_week,
            'performances': habit.this_weeks_performance
        }
        habit_data.append(habit_info)

    context = {
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'days_of_week': days_of_week,

        # list of dictionaries. Each dictionary has keys 'id', 'title', and 'performances'.
        # 'performances' is a dictionary of {date: performed (bool)} pairs.
        'habits': habit_data,
    }
    return render(request, 'app/habits.html', context)


@csrf_exempt
@require_POST
def daily_performance_update(request):
    """Update the daily performance of a habit."""
    data = json.loads(request.body)
    habit_id, date, performed = data['habitId'], data['date'], data['performed']

    # Get the DailyPerformance record for the habit and date and update it
    habit = Habit.objects.get(id=habit_id)
    daily_performance = habit.dailyperformance_set.get(date=date)
    daily_performance.performed = performed
    daily_performance.save()

    count = habit.count_this_week
    goal = habit.goal

    #TODO: update the current streak of the habit

    return JsonResponse({
        'success': True,
        'habitId': habit_id,
        'habitTitle': habit.title,
        'count': count,
        'goal': goal
    })


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
