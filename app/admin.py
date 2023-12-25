from django.contrib import admin
from .models import Event

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  list_display = ('title', 'details', 'date', 'location', 'creator', 'display_attendees')

  fieldsets = (
    (None, {
      'fields': ('title', 'details')
    }),
    ('Date and location', {
      'fields': ('date', 'location')
    }),
    ('Creator & Attendeses', {
      'fields': ('creator', 'attendees')
    }),
  )