from typing import Any
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .models import Event
# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
  context = {
    'future_events': Event.future().all(),
    'past_events': Event.past().all(),
  }
  return render(request, 'index.html', context=context)


class EventDetailView(generic.DetailView):
  model = Event

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context['user_is_attendee'] = self.object.is_attendee(self.request.user)
    context['user_is_creator'] = self.object.is_creator(self.request.user)
    return context


class EventCreateView(LoginRequiredMixin, CreateView):
  model = Event
  fields = ['title', 'details', 'date', 'location']
  success_url = reverse_lazy('index')

  def form_valid(self, form):
    form.instance.creator = self.request.user
    self.object = form.save()
    self.object.attendees.add(self.request.user)
    return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
  model = Event
  fields = ['title', 'details', 'date', 'location']
  success_url = reverse_lazy('index')

  def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    event = self.get_object()
    if request.user != event.creator:
      return self.handle_no_permission()
    return super().dispatch(request, *args, **kwargs)


@login_required
def event_delete(request: HttpRequest, pk: int) -> HttpResponse:
  event = Event.objects.get(id=pk)
  if event.creator == request.user:
    event.delete()
  return HttpResponseRedirect(reverse_lazy('index'))

  

def event_attend(request: HttpRequest, pk) -> HttpResponse:
  if request.user.is_authenticated:
    event = Event.objects.get(pk=pk)
    event.attendees.add(request.user)
    return redirect('event-detail', pk=pk)
  else:
    return HttpResponseForbidden('403 Forbidden')
  

def event_unattend(request: HttpRequest, pk) -> HttpResponse:
  if request.user.is_authenticated:
    if request.method == 'POST':
      event = get_object_or_404(Event, pk=pk)
      event.attendees.remove(request.user)
  
    return redirect('event-detail', pk=pk)
  else:
    return redirect('index')


class UserShow(LoginRequiredMixin, generic.ListView):
  model = Event
  template_name = 'app/user_show.html'

  def get_context_data(self) -> QuerySet[Any]:
    user = self.request.user

    return {
      'event_list': Event.objects.filter(creator=user),
      'attended_upcoming_events_list': user.attended_events.filter(date__gte=datetime.now()),
      'attended_past_events_list': user.attended_events.filter(date__lte=datetime.now()),
    }