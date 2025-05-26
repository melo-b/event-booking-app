from django.contrib import admin
from .models import UserProfile, Event, RSVP

# Register your models here.
admin.site.register(UserProfile)

admin.site.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'capacity', 'creator', 'attendee_count')
    list_filter = ('event_type', 'date')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('attendees',)

    def attendee_count(self, obj):
        return obj.attendees.count()
    attendee_count.short_description = 'RSVPs'
    
admin.site.register(RSVP)