from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    """Extended user profile with additional information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        """Return the username as string representation."""
        return self.user.username


class Event(models.Model):
    """Model representing an event that users can RSVP to."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(User, through='RSVP', related_name='events_attending')

    def is_full(self):
        """Check if the event has reached its capacity."""
        return self.attendees.count() >= self.capacity
    
    def clean(self):
        """Validate that the event doesn't exceed capacity."""
        if self.pk and self.attendees.count() > self.capacity:
            raise ValidationError("This event is already full.")
    
    def __str__(self):
        """Return a string representation of the event."""
        return f"{self.title} on {self.date.strftime('%Y-%m-%d')}"

    def available_slots(self):
        """Return the number of available slots for the event."""
        return self.capacity - self.rsvp_set.count()



class RSVP(models.Model):
    """Model representing a user's RSVP to an event."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Prevent duplicate RSVPs

    def __str__(self):
        """Return a string representation of the RSVP."""
        return f"{self.user.username} RSVP'd to {self.event.title}"