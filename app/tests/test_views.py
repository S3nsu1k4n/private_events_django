from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from app.models import Event
from datetime import datetime, timezone
# accounts/login/

class LoginTest(TestCase):
  """Tests the login view"""
  
  def test_view_url_exists_at_desired_location(self) -> None:
    """Checks if the url of the view exists"""
    response = self.client.get(reverse('login'))
    self.assertEqual(response.status_code, 200)

  def tests_correct_template(self) -> None:
    """Checks if the correct template is used"""
    response = self.client.get(reverse('login'))
    self.assertTemplateUsed(response, 'registration/login.html')

# accounts/logout/
    
class LogoutTest(TestCase):
  """Tests the logout view"""
  
  def test_view_url_exists_at_desired_location(self) -> None:
    """Checks if the url of the view exists"""
    response = self.client.get(reverse('logout'))
    self.assertEqual(response.status_code, 302)

# myevents/ (UserShow)

class MyEventsTest(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and save to database"""
    test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
    test_user.save()


  def test_redirect_if_not_logged_in(self):
    """Tests if redirect is returned if user is not logged in"""
    response = self.client.get(reverse('myevents'))

    self.assertRedirects(response, '/accounts/login/?next=/app/myevents/')

  def test_logged_in_uses_correct_template(self):
    """Tests if user is logged in correctly and get the correct templates"""
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    response = self.client.get(reverse('myevents'))

    # Check user is logged in
    self.assertEqual(str(response.context['user']), 'testuser')
    # Check that we got a response "success"
    self.assertEqual(response.status_code, 200)

    # Check we used correct template
    self.assertTemplateUsed(response, 'app/user_show.html')
    self.assertTemplateUsed(response, 'base_generic.html')


# events/{id}
class EventDetailViewTest(TestCase):
  """Tests the logout view"""
  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and save to database"""
    user = User.objects.create(username='testuser', password='testusertestuser')
    event = Event.objects.create(
       title='Test Event',
       details='Details about the event',
       date='2999-12-31T23:59Z',
       location='Test building',
       creator=user,
       )
    event.attendees.add(user)
  
  def test_view_url_exists_at_desired_location_event_exists(self) -> None:
    """Checks if the url of the view exists"""
    response = self.client.get(reverse('event-detail', kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 200)
  
  def test_view_url_exists_at_desired_location_event_not_exists(self) -> None:
    """Checks if the url of the view exists"""
    response = self.client.get(reverse('event-detail', kwargs={'pk': 999}))
    self.assertEqual(response.status_code, 404)


# events/create/
    
class EventCreateTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and save to database"""
    test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
    test_user.save()

  def test_redirect_if_not_logged_in(self) -> None:
    """Tests if redirect is returned if user is not logged in"""
    response = self.client.get(reverse('event_create'))
    self.assertRedirects(response, '/accounts/login/?next=/app/events/create')

  def test_logged_in_uses_correct_template(self) -> None:
    """Tests if user is logged in correctly and get the correct templates"""
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    response = self.client.get(reverse('event_create'))

    # Check user is logged in
    self.assertEqual(str(response.context['user']), 'testuser')
    # Check that we got a response "success"
    self.assertEqual(response.status_code, 200)

    # Check we used correct template
    self.assertTemplateUsed(response, 'app/event_form.html')
    self.assertTemplateUsed(response, 'base_generic.html')

  def test_form_submission(self) -> None:
    """Tests if the form correctly adds a new event"""
    user = User.objects.get(id=1)
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    form_data = {
      'title': 'Test Event',
      'details': 'Something informative',
      'date': '2039-12-29T12:12Z',
      'location': 'In the stars',
      'creator': user,
    }

    response = self.client.post(reverse('event_create'), data=form_data)
    # Check if the form submission is successful
    self.assertRedirects(response, reverse('index'))

    event = Event.objects.get(id=1)
    
    # check if create was succesful
    self.assertEqual(event.title, 'Test Event')
    self.assertEqual(event.details, 'Something informative')
    self.assertEqual(event.date, datetime(2039, 12, 29, 12, 12, tzinfo=timezone.utc))
    self.assertEqual(event.location, 'In the stars')
    self.assertEqual(event.creator, user)

# events/edit/
    
class EventEditViewTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and a event and save to database"""
    user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
    user.save()
    event = Event.objects.create(
       title='Test Event',
       details='Details about the event',
       date='2999-12-31T23:59Z',
       location='Test building',
       creator=user,
       )

  def test_redirect_if_not_logged_in(self) -> None:
    """Tests if redirect is returned if user is not logged in"""
    event_id = 1
    response = self.client.get(reverse('event-update', args=[event_id]))
    self.assertRedirects(response, f'/accounts/login/?next=/app/events/{event_id}/edit')

  def test_logged_in_uses_correct_template(self) -> None:
    """Tests if user is logged in correctly and get the correct templates"""
    event_id = 1
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    response = self.client.get(reverse('event-update', args=[event_id]))

    # Check user is logged in
    self.assertEqual(str(response.context['user']), 'testuser')
    # Check that we got a response "success"
    self.assertEqual(response.status_code, 200)

    # Check we used correct template
    self.assertTemplateUsed(response, 'app/event_form.html')
    self.assertTemplateUsed(response, 'base_generic.html')

  def test_form_submission(self) -> None:
    """Tests if the form correctly updates a specific event"""
    event_id = 1
    event = Event.objects.get(id=event_id)
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    form_data = {
      'title': 'Test Event (edited)',
      'location': 'Different Test Building',
      'details': event.details,
      'date': event.date,
    }

    response = self.client.post(reverse('event-update', args=[event_id]), data=form_data)
    
    # Check if the form submission is successful
    self.assertRedirects(response, reverse('index'))

    event = Event.objects.get(id=1)
    
    # check if edit was succesful
    self.assertEqual(event.title, 'Test Event (edited)')
    self.assertEqual(event.location, 'Different Test Building')

# events/delete/

class EventEditViewTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and a event and save to database"""
    user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
    user.save()
    event = Event.objects.create(
       title='Test Event',
       details='Details about the event',
       date='2999-12-31T23:59Z',
       location='Test building',
       creator=user,
       )

  def test_redirect_if_not_logged_in(self) -> None:
      """Tests if redirect is returned if user is not logged in"""
      event_id = 1
      response = self.client.get(reverse('event-delete', args=[event_id]))
      self.assertRedirects(response, f'/accounts/login/?next=/app/events/{event_id}/delete')
      self.assertEqual(len(Event.objects.all()), 1)

  def test_redirect_if_delete(self) -> None:
    """Tests if user is logged in correctly and get the correct templates"""
    event_id = 1
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    response = self.client.get(reverse('event-delete', args=[event_id]))

    # Check that we got a redirect
    self.assertRedirects(response, reverse('index'))

# events/attend/
    
class EventEditViewTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and a event and save to database"""
    user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
    user.save()
    event = Event.objects.create(
       title='Test Event',
       details='Details about the event',
       date='2999-12-31T23:59Z',
       location='Test building',
       creator=user,
       )
    
  def test_forbidden_if_not_logged_in(self) -> None:
      """Tests if forbidden is returned if user is not logged in"""
      event_id = 1
      response = self.client.get(reverse('event-attend', args=[event_id]))
      self.assertEqual(response.status_code, 403)
  
  def test_redirect_if_logged_in(self) -> None:
      """Tests if redirect is returned if user is logged in"""
      event_id = 1
      login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
      response = self.client.get(reverse('event-attend', args=[event_id]))

      # check if redirects if logged in
      self.assertRedirects(response, reverse('event-detail', kwargs={'pk': event_id}))

  def test_adds_user_to_attendees(self) -> None:
    event_id = 1
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    event = Event.objects.get(id=event_id)

    # Check if there are no attendees yet
    self.assertEqual(len(event.attendees.all()), 0)

    response = self.client.post(reverse('event-attend', args=[event_id]))

    # check if redirects if logged in
    self.assertRedirects(response, reverse('event-detail', kwargs={'pk': event_id}))

    # check if we now have a new attendee
    self.assertEqual(len(event.attendees.all()), 1)

# events/unattend/
    
class EventEditViewTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    """Create user and a event and save to database"""
    user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
    user.save()
    event = Event.objects.create(
       title='Test Event',
       details='Details about the event',
       date='2999-12-31T23:59Z',
       location='Test building',
       creator=user,
       )
    event.attendees.add(user)
    
    
  def test_forbidden_if_not_logged_in(self) -> None:
      """Tests if forbidden is returned if user is not logged in"""
      event_id = 1
      response = self.client.get(reverse('event-unattend', args=[event_id]))
      self.assertEqual(response.status_code, 403)
  
  def test_redirect_if_logged_in(self) -> None:
      """Tests if redirect is returned if user is logged in"""
      event_id = 1
      login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
      response = self.client.get(reverse('event-unattend', args=[event_id]))

      # check if redirects if logged in
      self.assertRedirects(response, reverse('event-detail', kwargs={'pk': event_id}))

  def test_adds_user_to_attendees(self) -> None:
    event_id = 1
    login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
    event = Event.objects.get(id=event_id)

    # Check if there is an attendee
    self.assertEqual(len(event.attendees.all()), 1)

    response = self.client.post(reverse('event-unattend', args=[event_id]))

    # check if redirects if logged in
    self.assertRedirects(response, reverse('event-detail', kwargs={'pk': event_id}))

    # check if attendee is now unattended
    self.assertEqual(len(event.attendees.all()), 0)
