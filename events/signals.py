from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Event
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=Event.attendees.through)
def rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    """Send confirmation email when user RSVPs to an event."""
    if action == "post_add":
        for user_pk in pk_set:
            try:
                user = User.objects.get(pk=user_pk)
                
                # In a real application, you would send an actual email
                # For now, we'll just log it and simulate the email sending
                subject = f"RSVP Confirmation for {instance.title}"
                message = f"""
Hello {user.username},

Thank you for RSVPing to "{instance.title}"!

Event Details:
- Date: {instance.date}
- Location: {instance.location}
- Event Type: {instance.event_type}

We look forward to seeing you there!

Best regards,
Event Booking Team
                """
                
                # Simulate email sending (in production, uncomment the next line)
                # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                
                logger.info(f"RSVP confirmation email sent to: {user.email} for event '{instance.title}'")
                print(f"Confirmation email would be sent to: {user.email} for event '{instance.title}'")
                
            except User.DoesNotExist:
                logger.error(f"User with pk={user_pk} not found for RSVP confirmation")
            except Exception as e:
                logger.error(f"Error sending RSVP confirmation email: {str(e)}")
