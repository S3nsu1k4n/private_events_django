from django.test import TestCase
from app.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()

class EventModelTest(TestCase):
  """Tests the event model"""

  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username='testuser', password='testusertestuser')
    event = Event.objects.create(
       title='Test Event',
       details='Details about the event',
       date='2999-12-31T23:59Z',
       location='Test building',
       creator=user,
       )
    event.attendees.add(user)

  def get_event_field(self, event_id: int, field_name: str):
    return Event.objects.get(id=event_id)._meta.get_field(field_name)

  def check_verbose_name(self, field_name: str, verbose_name: str) -> None:
    field_label = self.get_event_field(event_id=1, field_name=field_name).verbose_name
    self.assertEqual(field_label, verbose_name)

  def check_max_length(self, field_name: str, max_length: int) -> None:
    field_length = self.get_event_field(event_id=1, field_name=field_name).max_length
    self.assertEqual(field_length, max_length)

  def check_uniqueness(self, field_name: str, unique: bool) -> None:
    field_unique = self.get_event_field(event_id=1, field_name=field_name).unique
    self.assertEqual(field_unique, unique)

  def check_auto_now_add(self, field_name: str, auto_now_add: bool) -> None:
    value = self.get_event_field(event_id=1, field_name=field_name).auto_now_add
    self.assertEqual(value, auto_now_add)
  
  def check_auto_now(self, field_name: str, auto_now: bool) -> None:
    value = self.get_event_field(event_id=1, field_name=field_name).auto_now
    self.assertEqual(value, auto_now)

  # TITLE

  def test_title_label(self):
      """tests the title field"""
      self.check_verbose_name(field_name='title', verbose_name='Title')

  def test_title_length(self):
    """tests the title fields max length"""
    self.check_max_length(field_name='title', max_length=100)

  def test_title_uniqueness(self):
    """tests the title fields uniqueness"""
    self.check_uniqueness(field_name='title', unique=True)

  # DETAILS
    
  def test_details_label(self):
    """tests the detail field"""
    self.check_verbose_name(field_name='details', verbose_name='Details')

  def test_details_length(self):
    """tests the details fields max length"""
    self.check_max_length(field_name='details', max_length=None)

  def test_details_uniqueness(self):
    """tests the details fields uniqueness"""
    self.check_uniqueness(field_name='details', unique=False)
    
  # Date
    
  def test_date_label(self):
    """tests the detail field"""
    self.check_verbose_name(field_name='date', verbose_name='Date')

  def test_date_length(self):
    """tests the details fields max length"""
    self.check_max_length(field_name='date', max_length=None)

  def test_date_uniqueness(self):
    """tests the details fields uniqueness"""
    self.check_uniqueness(field_name='date', unique=False)
    
  # Location
    
  def test_location_label(self):
    """tests the location field"""
    self.check_verbose_name(field_name='location', verbose_name='Location')

  def test_location_length(self):
    """tests the location fields max length"""
    self.check_max_length(field_name='location', max_length=100)

  def test_location_uniqueness(self):
    """tests the location fields uniqueness"""
    self.check_uniqueness(field_name='location', unique=False)

  # CREATED_AT
  
  def test_created_at_auto_now_add(self):
    """tests the created_at fields auto now add"""
    self.check_auto_now_add(field_name='created_at', auto_now_add=True)

  # UPDATED_AT
    
  def test_updated_at_auto_now(self):
    """tests the updated_at fields auto now add"""
    self.check_auto_now(field_name='updated_at', auto_now=True)

  # __str__()
    
  def test___str__(self):
    """Checks the __str__() method"""
    event = Event.objects.get(id=1)
    self.assertEqual(str(event), 'Test Event')
  
  # display_attendees()
    
  def test_display_attendees(self):
    """Checks the display_attendees() method"""
    user = User.objects.get(id=1)
    attendees = Event.objects.get(id=1).display_attendees()
    self.assertEqual(attendees, user.username)
  
  # is_creator()
    
  def test_is_creator(self):
    """Checks the is_creator() method"""
    event = Event.objects.get(id=1)
    user = User.objects.get(id=1)

    self.assertEqual(event.is_creator(user), True)

    self.assertEqual(event.is_creator('Random guy'), False)
  
  # is_attendee()
    
  def test_is_attendee(self):
    """Checks the is_attendee() method"""
    event = Event.objects.get(id=1)
    user = User.objects.get(id=1)

    self.assertEqual(event.is_attendee(user), True)

    self.assertEqual(event.is_attendee('Random guy'), False)
  
  # past() classmethod
    
  def test_past_classmethod(self):
    """Checks the past() classmethod"""
    past_events = Event.past()

    self.assertEqual(len(past_events), 0)
  
  # future() classmethod
    
  def test_future_classmethod(self):
    """Checks the future() classmethod"""
    future_events = Event.future()

    self.assertEqual(len(future_events), 1)
