from django.urls import path
from . import views as app_views

urlpatterns = [
    path('', app_views.home, name='app-home'),

    path('habits/', app_views.habits, name='app-habits'),
    path('habits/new_week/', app_views.week_reset, name='habit-new-week'),
    path('habits/new/', app_views.HabitCreateView.as_view(), name='habit-create'),
    path('habits/<int:pk>/update/', app_views.HabitUpdateView.as_view(), name='habit-update'),
    path('habits/<int:pk>/delete/', app_views.HabitDeleteView.as_view(), name='habit-delete'),

    path('journals/', app_views.JournalListView.as_view(), name='app-journals'),
    path('journals/<int:pk>/', app_views.JournalDetailView.as_view(), name='journal-detail'),
    path('journals/new/', app_views.JournalCreateView.as_view(), name='journal-create'),
    path('journals/<int:pk>/update/', app_views.JournalUpdateView.as_view(), name='journal-update'),
    path('journals/<int:pk>/delete/', app_views.JournalDeleteView.as_view(), name='journal-delete'),

]
