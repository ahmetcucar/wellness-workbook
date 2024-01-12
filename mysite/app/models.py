from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)  # Optional title
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or f"Journal on {self.date_posted.strftime('%m.%d.%Y')}"

    # This method tells django how to find the url to any specific instance of a post
    # The reverse function returns the full url as a string
    def get_absolute_url(self):
        return reverse('journal-detail', kwargs={'pk': self.pk})


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    goal = models.PositiveIntegerField(default=7)  # Number of times the habit is targeted per week
    current_streak = models.PositiveIntegerField(default=0)  # Current streak of the habit

    def __str__(self):
        return self.title

    @property
    def this_weeks_performance(self):
        """
        Calculate performance from Monday to Sunday of the current week.
        Returns a dictionary of {date: performed (bool)} pairs.
        """
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timezone.timedelta(days=6)  # Sunday
        days_of_week = [start_of_week + timezone.timedelta(days=i) for i in range(7)]
        for day in days_of_week:
            if not self.dailyperformance_set.filter(date=day).exists():
                DailyPerformance.objects.create(habit=self, date=day)
        performances = self.dailyperformance_set.filter(date__range=[start_of_week, end_of_week])
        return {perf.date: perf.performed for perf in performances}


"""
TODO:
Initialization of DailyPerformance Records:
You may need to initialize DailyPerformance records for each habit at the start
of the week or when a new habit is created.
"""
class DailyPerformance(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    performed = models.BooleanField(default=False)  # True if the habit was performed on this date

    def __str__(self):
        return f"{self.habit.title} - {self.date} - {'Done' if self.performed else 'Not Done'}"
