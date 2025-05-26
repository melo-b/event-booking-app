from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Event
from django.contrib.auth.models import User

@receiver(m2m_changed, sender=Event.attendees.through)
def rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_pk in pk_set:
            user = User.objects.get(pk=user_pk)
            print(f"Confirmation email would be sent to: {user.email} for event '{instance.title}'")
