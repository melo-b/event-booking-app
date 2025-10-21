from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Event, RSVP, UserProfile


class EventModelTest(TestCase):
    """Test cases for Event model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            event_type='Workshop',
            date=timezone.now() + timedelta(days=1),
            location='Test Location',
            capacity=10,
            creator=self.user
        )

    def test_event_creation(self):
        """Test event creation."""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.creator, self.user)
        self.assertEqual(self.event.capacity, 10)

    def test_event_string_representation(self):
        """Test event string representation."""
        expected = f"{self.event.title} on {self.event.date.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.event), expected)

    def test_is_full_method(self):
        """Test is_full method."""
        self.assertFalse(self.event.is_full())
        
        # Add attendees up to capacity
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
            self.event.attendees.add(user)
        
        self.assertTrue(self.event.is_full())

    def test_available_slots_method(self):
        """Test available_slots method."""
        self.assertEqual(self.event.available_slots(), 10)
        
        # Add one attendee
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.event.attendees.add(user2)
        
        self.assertEqual(self.event.available_slots(), 9)

    def test_clean_method_with_overcapacity(self):
        """Test clean method prevents overcapacity."""
        # Add attendees beyond capacity
        for i in range(15):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
            self.event.attendees.add(user)
        
        with self.assertRaises(ValidationError):
            self.event.full_clean()


class RSVPModelTest(TestCase):
    """Test cases for RSVP model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            event_type='Workshop',
            date=timezone.now() + timedelta(days=1),
            location='Test Location',
            capacity=10,
            creator=self.user
        )

    def test_rsvp_creation(self):
        """Test RSVP creation."""
        rsvp = RSVP.objects.create(user=self.user, event=self.event)
        self.assertEqual(rsvp.user, self.user)
        self.assertEqual(rsvp.event, self.event)
        self.assertIsNotNone(rsvp.timestamp)

    def test_rsvp_string_representation(self):
        """Test RSVP string representation."""
        rsvp = RSVP.objects.create(user=self.user, event=self.event)
        expected = f"{self.user.username} RSVP'd to {self.event.title}"
        self.assertEqual(str(rsvp), expected)

    def test_unique_constraint(self):
        """Test that duplicate RSVPs are prevented."""
        RSVP.objects.create(user=self.user, event=self.event)
        
        # Try to create duplicate RSVP
        with self.assertRaises(Exception):  # IntegrityError
            RSVP.objects.create(user=self.user, event=self.event)


class EventViewsTest(TestCase):
    """Test cases for event views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            event_type='Workshop',
            date=timezone.now() + timedelta(days=1),
            location='Test Location',
            capacity=10,
            creator=self.user
        )

    def test_event_list_view(self):
        """Test event list view."""
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_detail_view(self):
        """Test event detail view."""
        response = self.client.get(reverse('event_detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)
        self.assertContains(response, self.event.description)

    def test_event_create_view_requires_login(self):
        """Test that event creation requires login."""
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_event_create_view_authenticated(self):
        """Test event creation for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 200)

    def test_event_create_post(self):
        """Test event creation via POST."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'event_type': 'Conference',
            'date': timezone.now() + timedelta(days=2),
            'location': 'New Location',
            'capacity': 20
        }
        response = self.client.post(reverse('event_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Check if event was created
        new_event = Event.objects.get(title='New Event')
        self.assertEqual(new_event.creator, self.user)

    def test_event_edit_view_permission(self):
        """Test that only event creator can edit."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        # Try to edit as other user
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('event_edit', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_event_delete_view_permission(self):
        """Test that only event creator can delete."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        # Try to delete as other user
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('event_delete', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_rsvp_requires_login(self):
        """Test that RSVP requires login."""
        response = self.client.post(reverse('rsvp_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_rsvp_success(self):
        """Test successful RSVP."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('rsvp_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after RSVP
        
        # Check if RSVP was created
        self.assertTrue(self.user in self.event.attendees.all())

    def test_rsvp_duplicate_prevention(self):
        """Test that duplicate RSVPs are prevented."""
        self.client.login(username='testuser', password='testpass123')
        
        # First RSVP
        self.client.post(reverse('rsvp_event', kwargs={'pk': self.event.pk}))
        
        # Try to RSVP again
        response = self.client.post(reverse('rsvp_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)  # Should still redirect but with message

    def test_search_functionality(self):
        """Test search functionality."""
        response = self.client.get(reverse('event_list'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_filter_by_type(self):
        """Test filtering by event type."""
        response = self.client.get(reverse('event_list'), {'type': 'Workshop'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_filter_by_date(self):
        """Test filtering by date."""
        tomorrow = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('event_list'), {'date': tomorrow})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')


class UserRegistrationTest(TestCase):
    """Test cases for user registration."""
    
    def test_register_view(self):
        """Test registration view."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        """Test user registration via POST."""
        data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())


class EventCapacityTest(TestCase):
    """Test cases for event capacity functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            event_type='Workshop',
            date=timezone.now() + timedelta(days=1),
            location='Test Location',
            capacity=2,  # Small capacity for testing
            creator=self.user
        )

    def test_rsvp_when_full(self):
        """Test RSVP behavior when event is full."""
        # Fill up the event
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
        self.event.attendees.add(user1, user2)
        
        # Try to RSVP as another user
        user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        self.client.login(username='user3', password='testpass123')
        
        response = self.client.post(reverse('rsvp_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 302)  # Should redirect with error message
