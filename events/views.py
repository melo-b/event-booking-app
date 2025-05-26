from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, RSVP
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.rsvp_set.filter(user=request.user).exists():
        messages.warning(request, "You have already RSVP’d to this event.")
    elif event.rsvp_set.count() >= event.capacity:
        messages.error(request, "Sorry, this event is full.")
    else:
        RSVP.objects.create(user=request.user, event=event)
        messages.success(request, "RSVP successful!")

    return redirect('event_detail', pk=pk)