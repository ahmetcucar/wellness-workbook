from django.test import TestCase
from django.utils import timezone
from .models import Habit, DailyPerformance
from django.contrib.auth.models import User

# Create your tests here.
class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.habit = Habit.objects.create(user=self.user, title='test habit', goal=7)

    ########### STREAK TESTS ####################################################

    def test_streak_with_no_breaks(self):
        """This test checks the scenario where the habit has been performed consistently
        every day for a week."""
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        for i in range(7):
            date = start_date + timezone.timedelta(days=i)
            DailyPerformance.objects.create(habit=self.habit, date=date, performed=True)

        self.assertEqual(self.habit.current_streak, 7)

    def test_streak_long(self):
        """This test checks the scenario where the habit has been performed consistently
        every day for a month."""
        start_date = timezone.now().date() - timezone.timedelta(days=30)
        for i in range(30):
            date = start_date + timezone.timedelta(days=i)
            DailyPerformance.objects.create(habit=self.habit, date=date, performed=True)

        self.assertEqual(self.habit.current_streak, 30)

    def test_streak_with_break(self):
        """ From the past 7 days, the habit has been performed for 4 days,
        then a break on the 5th day, then 2 more days where it was performed."""
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        for i in range(7):
            date = start_date + timezone.timedelta(days=i)
            DailyPerformance.objects.create(habit=self.habit, date=date, performed=True if i != 4 else False)

        self.assertEqual(self.habit.current_streak, 2)

    def test_streak_start_partway_through_week(self):
        """This test checks the scenario where the habit has been performed
        for the past 4 days."""
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        for i in range(3):
            date = start_date + timezone.timedelta(days=i)
            DailyPerformance.objects.create(habit=self.habit, date=date, performed=False)
        for i in range(3, 7):
            date = start_date + timezone.timedelta(days=i)
            DailyPerformance.objects.create(habit=self.habit, date=date, performed=True)
        self.assertEqual(self.habit.current_streak, 4)

    def test_streak_with_no_performances(self):
        """This test checks the scenario where the habit has not been performed
        for the past week."""
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        for i in range(7):
            date = start_date + timezone.timedelta(days=i)
            DailyPerformance.objects.create(habit=self.habit, date=date, performed=False)

        self.assertEqual(self.habit.current_streak, 0)

    def test_streak_with_no_records(self):
        """This test checks the scenario where the habit has no records."""
        self.assertEqual(self.habit.current_streak, 0)