from django.urls import path
from . import views as app_views

urlpatterns = [
    path('', app_views.home, name='app-home'),
    path('habits/', app_views.habits, name='app-habits'),
    path('journals/', app_views.JournalListView.as_view(), name='app-journals'),
    path('journals/<int:pk>/', app_views.JournalDetailView.as_view(), name='journal-detail'),
    path('journals/new/', app_views.JournalCreateView.as_view(), name='journal-create'),
    path('journals/<int:pk>/update/', app_views.JournalUpdateView.as_view(), name='journal-update'),

]
