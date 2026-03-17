from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Event, RSVP

class EventSafetyTests(TestCase):
    """
    Test suite focused on data integrity, concurrency limits, 
    and overbooking prevention.
    """
    
    def setUp(self):
        """Set up the baseline data for every test."""
        # Create test users
        self.user1 = User.objects.create_user(username='tester1', password='password')
        self.user2 = User.objects.create_user(username='tester2', password='password')
        
        # Create a test event with a strict capacity of exactly 1
        self.event = Event.objects.create(
            title="Safety Engineering Summit",
            description="Testing capacity limits.",
            event_type="Conference",
            date=timezone.now() + timedelta(days=5),
            location="Main Hall",
            capacity=1,  # Only 1 ticket available!
            creator=self.user1
        )

    def test_prevent_double_rsvp(self):
        """Test that the database strictly blocks a user from RSVPing twice."""
        
        # 1. First RSVP should succeed perfectly
        RSVP.objects.create(user=self.user1, event=self.event)
        
        # 2. Second RSVP from the SAME user should trigger the database lock
        # The test passes if the IntegrityError is successfully raised
        with self.assertRaises(IntegrityError):
            RSVP.objects.create(user=self.user1, event=self.event)

    def test_enforce_capacity_limit(self):
        """Test that the model validation blocks overbooking."""
        
        # 1. User 1 takes the only available spot
        self.event.attendees.add(self.user1)
        self.event.full_clean()  # This should pass without errors
        
        # 2. User 2 tries to RSVP to the full event
        self.event.attendees.add(self.user2)
        
        # 3. Validation should catch the overbooking and raise an error
        # The test passes if the ValidationError is successfully raised
        with self.assertRaises(ValidationError):
            self.event.full_clean()