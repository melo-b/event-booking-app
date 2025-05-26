from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, RSVP
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def event_list(request):
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
            pass  # Ignore invalid date input

    return render(request, 'events/event_list.html', {
        'events': events,
        'query': query or '',
        'selected_type': event_type or '',
        'selected_date': date or '',
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def rsvp_event(request, pk):
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
        else:
            messages.success(request, "You have successfully RSVPed!")

    return redirect('event_detail', pk=pk)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'event_type', 'date', 'location', 'capacity']
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'event_type', 'date', 'location', 'capacity']
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.creator


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')
    template_name = 'events/event_confirm_delete.html'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.creator

