from django.urls import path
from .views import home, habits, JournalListView, JournalDetailView

urlpatterns = [
    path('', home, name='app-home'),
    path('habits/', habits, name='app-habits'),
    path('journals/', JournalListView.as_view(), name='app-journals'),
    path('journals/<int:pk>/', JournalDetailView.as_view(), name='journal-detail'),
]
