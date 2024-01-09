from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.views import generic

from .models import Event
# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
  events = Event.objects.all()
  context = {
    'events': events,
  }
  return render(request, 'index.html', context=context)

class EventDetailView(generic.DetailView):
  model = Event

class UserShow(generic.ListView):
  model = Event
  template_name = 'app/user_show.html'

  def get_queryset(self) -> QuerySet[Any]:
    return (
      Event.objects.filter(creator=self.request.user)
    )