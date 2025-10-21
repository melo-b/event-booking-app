from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('event/<int:pk>/cancel-rsvp/', views.cancel_rsvp, name='cancel_rsvp'),
    path('event/new/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('register/', views.register, name='register'),
]
