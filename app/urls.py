from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('events/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
  path('myevents/', views.UserShow.as_view(), name='myevents'),
  path('events/create', views.EventCreateView.as_view(), name='event_create'),
  path('events/<int:pk>/attend', views.event_attend, name='event-attend'),
  path('events/<int:pk>/unattend', views.event_unattend, name='event-unattend'),
]