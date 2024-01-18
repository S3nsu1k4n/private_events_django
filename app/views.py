from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

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
    self.object = form.save()
    self.object.attendees.add(self.request.user)
    return super().form_valid(form)


class UserShow(generic.ListView):
  model = Event
  template_name = 'app/user_show.html'

  def get_context_data(self) -> QuerySet[Any]:
    user = self.request.user
    if user.is_anonymous:
      return {}
    
    return {
      'event_list': Event.objects.filter(creator=user),
      'attended_upcoming_events_list': user.attended_events.filter(date__gte=datetime.now()),
      'attended_past_events_list': user.attended_events.filter(date__lte=datetime.now()),
    }
  

def event_attend(request: HttpRequest, pk) -> HttpResponse:
  event = Event.objects.get(pk=pk)
  event.attendees.add(request.user)
  return redirect('event-detail', pk=pk)
  

def event_unattend(request: HttpRequest, pk) -> HttpResponse:
  if request.method == 'POST':
    event = get_object_or_404(Event, pk=pk)
    event.attendees.remove(request.user)
  
  return redirect('event-detail', pk=pk)