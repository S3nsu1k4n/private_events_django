from django.db import models
from django.conf import settings
from django.urls import reverse

from datetime import datetime
# Create your models here.

class Event(models.Model):
  """Event Model
  
  Attributes
  ----------
  title : CharField
  details : TextField
  date : DateTimeField
  location : CharField
  creator : ForeignKey(User)
  attendees : ManyToMany(User)
  created_at : DateTime
  updated_at : DateTime
  """
  title = models.CharField('Title', max_length=100, unique=True, help_text='Title of the event')
  details = models.TextField('Details', help_text='Details about the event')
  date = models.DateTimeField('Date', help_text='When the event is planned to start')
  location = models.CharField('Location', max_length=100, help_text='Where the event will be held')
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='The creator of the event', related_name='created_events')
  attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text='Attendees of the event', related_name='attended_events')

  created_at = models.DateTimeField(auto_now_add=True, help_text='When this event entry was created')
  updated_at = models.DateTimeField(auto_now=True, help_text='When the event entry was updated the last time')

  def get_absolute_url(self):
    return reverse('event-detail', args=[str(self.id)])

  def __str__(self) -> str:
    return self.title
  
  def display_attendees(self):
    """Creating a string of attendees. This is required to display attendees in Admin."""
    return ', '.join(user.username for user in self.attendees.all()[:3])
  
  display_attendees.short_description = 'Attendees'

  def is_attendee(self, user: str) -> bool:
    return True if self.attendees.filter(username=user) else False
  
  def is_creator(self, user: str) -> bool:
    return True if self.creator == user else False

  @classmethod
  def past(self):
    return self.objects.filter(date__lte=datetime.now())

  @classmethod
  def future(self):
    return self.objects.filter(date__gte=datetime.now())