from django.contrib import admin
from .models import UserProfile, Event, RSVP

# Register your models here.
admin.site.register(UserProfile)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'capacity', 'creator', 'attendee_count')
    list_filter = ('event_type', 'date')
    search_fields = ('title', 'description', 'location')
    # Note: filter_horizontal cannot be used with ManyToManyField that has a custom through model

    def attendee_count(self, obj):
        return obj.attendees.count()
    attendee_count.short_description = 'RSVPs'

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'timestamp')
    list_filter = ('timestamp', 'event__event_type')
    search_fields = ('user__username', 'event__title')