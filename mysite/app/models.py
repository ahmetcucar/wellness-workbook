from django.db import models
from django.db.models import Max, Min
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


# TODO: test all the properties and methods of the Habit model
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    goal = models.PositiveIntegerField(default=7)  # Number of times the habit is targeted per week

    def __str__(self):
        return self.title


    @property
    def current_streak(self):
        """
        Calculate the current streak of the habit. The streak is the number of
        consecutive days up to today that the habit has been performed. If a day
        is missed, the streak resets.
        """
        today = timezone.now().date()

        # count the number of times the habit was performed consecutively from yesterday going back
        d = today - timezone.timedelta(days=1)
        streak = 0
        while True:
            try:
                perf = self.dailyperformance_set.get(date=d)
                if perf.performed:
                    streak += 1
                    d -= timezone.timedelta(days=1)
                else:
                    break
            except DailyPerformance.DoesNotExist:
                break

        # if the habit was performed today, add 1 to the streak
        try:
            perf = self.dailyperformance_set.get(date=today)
            if perf.performed:
                streak += 1
        except DailyPerformance.DoesNotExist:
            pass

        return streak



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

    @property
    def count_this_week(self):
        """Return the number of times the habit was performed this week."""
        return sum(self.this_weeks_performance.values())



class DailyPerformance(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    performed = models.BooleanField(default=False)  # True if the habit was performed on this date

    def __str__(self):
        return f"{self.habit.title} - {self.date} - {'Done' if self.performed else 'Not Done'}"
