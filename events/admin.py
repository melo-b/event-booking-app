from django.contrib import admin
from .models import UserProfile, Event, RSVP

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(RSVP)