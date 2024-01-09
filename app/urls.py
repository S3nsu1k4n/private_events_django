from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
  path('myevents/', views.UserShow.as_view(), name='myevents'),
]