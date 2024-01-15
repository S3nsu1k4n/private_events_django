from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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

class EventCreateView(LoginRequiredMixin,  CreateView):
  model = Event
  fields = ['title', 'details', 'date', 'location']
  success_url = reverse_lazy('index')

  def form_valid(self, form):
    form.instance.creator = self.request.user
    return super().form_valid(form)

class UserShow(generic.ListView):
  model = Event
  template_name = 'app/user_show.html'

  def get_queryset(self) -> QuerySet[Any]:
    user = self.request.user
    if user.is_anonymous:
      return []
    
    return (
      Event.objects.filter(creator=user)
    )