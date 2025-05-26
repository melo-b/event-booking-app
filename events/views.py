from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, RSVP
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


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

