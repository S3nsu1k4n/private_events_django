from django.db import models
from django.conf import settings
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

  def __str__(self) -> str:
    return self.title