from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

logger = logging.getLogger(__name__)


# Create your views here.

def event_list(request):
    """Display list of upcoming events with search and filtering capabilities."""
    try:
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')

        query = request.GET.get('q')
        event_type = request.GET.get('type')
        date = request.GET.get('date')

        if query:
            events = events.filter(title__icontains=query)

        if event_type:
            events = events.filter(event_type=event_type)

        if date:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d")
                events = events.filter(date__date=parsed_date.date())
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD format.")
                logger.warning(f"Invalid date format received: {date}")

        # Add pagination
        paginator = Paginator(events, 10)
        page_number = request.GET.get('page')
        try:
            events = paginator.page(page_number)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        return render(request, 'events/event_list.html', {
            'events': events,
            'query': query or '',
            'selected_type': event_type or '',
            'selected_date': date or '',
        })
    except Exception as e:
        logger.error(f"Error in event_list view: {str(e)}")
        messages.error(request, "An error occurred while loading events. Please try again.")
        return render(request, 'events/event_list.html', {
            'events': Event.objects.none(),
            'query': '',
            'selected_type': '',
            'selected_date': '',
        })

def event_detail(request, pk):
    """Display detailed information about a specific event."""
    try:
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'events/event_detail.html', {'event': event})
    except Http404:
        logger.warning(f"Event with pk={pk} not found")
        raise
    except Exception as e:
        logger.error(f"Error in event_detail view for pk={pk}: {str(e)}")
        messages.error(request, "An error occurred while loading the event details.")
        return redirect('event_list')


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f"Account created successfully for {user.username}. Please log in.")
                logger.info(f"New user registered: {user.username}")
                return redirect('login')
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                messages.error(request, "An error occurred during registration. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def rsvp_event(request, pk):
    """Handle RSVP to an event."""
    try:
        event = get_object_or_404(Event, pk=pk)

        if request.user in event.attendees.all():
            messages.info(request, "You've already RSVPed to this event.")
        elif event.is_full():
            messages.error(request, "Sorry, this event is full.")
        else:
            event.attendees.add(request.user)
            try:
                event.full_clean()  # Triggers model validation
            except ValidationError as e:
                event.attendees.remove(request.user)
                messages.error(request, str(e))
                logger.warning(f"RSVP validation failed for user {request.user.username} on event {event.title}: {str(e)}")
            else:
                messages.success(request, "You have successfully RSVPed!")
                logger.info(f"User {request.user.username} RSVPed to event {event.title}")

        return redirect('event_detail', pk=pk)
    except Http404:
        logger.warning(f"Event with pk={pk} not found for RSVP")
        raise
    except Exception as e:
        logger.error(f"Error in rsvp_event view for pk={pk}: {str(e)}")
        messages.error(request, "An error occurred while processing your RSVP. Please try again.")
        return redirect('event_detail', pk=pk)


@login_required
def cancel_rsvp(request, pk):
    """Handle RSVP cancellation for an event."""
    try:
        event = get_object_or_404(Event, pk=pk)

        if request.user not in event.attendees.all():
            messages.info(request, "You haven't RSVPed to this event.")
        else:
            event.attendees.remove(request.user)
            messages.success(request, "You have successfully cancelled your RSVP.")
            logger.info(f"User {request.user.username} cancelled RSVP for event {event.title}")

        return redirect('event_detail', pk=pk)
    except Http404:
        logger.warning(f"Event with pk={pk} not found for RSVP cancellation")
        raise
    except Exception as e:
        logger.error(f"Error in cancel_rsvp view for pk={pk}: {str(e)}")
        messages.error(request, "An error occurred while cancelling your RSVP. Please try again.")
        return redirect('event_detail', pk=pk)


class EventCreateView(LoginRequiredMixin, CreateView):
    """View for creating new events. Requires user authentication."""
    model = Event
    fields = ['title', 'description', 'event_type', 'date', 'location', 'capacity']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        """Set the event creator to the current user."""
        form.instance.creator = self.request.user
        logger.info(f"User {self.request.user.username} created event: {form.instance.title}")
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating existing events. Only the event creator can edit."""
    model = Event
    fields = ['title', 'description', 'event_type', 'date', 'location', 'capacity']
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        """Log the event update."""
        logger.info(f"User {self.request.user.username} updated event: {form.instance.title}")
        return super().form_valid(form)

    def test_func(self):
        """Test if the current user is the creator of the event."""
        event = self.get_object()
        return self.request.user == event.creator


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting events. Only the event creator can delete."""
    model = Event
    success_url = reverse_lazy('event_list')
    template_name = 'events/event_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        """Log the event deletion before deleting."""
        event = self.get_object()
        logger.info(f"User {request.user.username} deleted event: {event.title}")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        """Test if the current user is the creator of the event."""
        event = self.get_object()
        return self.request.user == event.creator

