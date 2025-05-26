from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(User, through='RSVP', related_name='events_attending')

    def is_full(self):
        return self.attendees.count() >= self.capacity
    
    def clean(self):
        if self.pk and self.attendees.count() > self.capacity:
            raise ValidationError("This event is already full.")
    
    def __str__(self):
        return f"{self.title} on {self.date.strftime('%Y-%m-%d')}"

    def available_slots(self):
        return self.capacity - self.rsvp_set.count()



class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Prevent duplicate RSVPs

    def __str__(self):
        return f"{self.user.username} RSVP'd to {self.event.title}"