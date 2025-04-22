from django.urls import path
from . import views as eventsViews

urlpatterns = [
    path('', eventsViews.events, name='events'),
    path('create/', eventsViews.create_event, name='create_event'),
    path('<int:event_id>/', eventsViews.event_view, name='event_view'),
    path('<int:event_id>/delete/', eventsViews.delete_event, name='delete_event'),
    path('<int:event_id>/register/', eventsViews.register, name='register_event'),
    path('<int:event_id>/unregister/', eventsViews.unregister, name='unregister_event'),
    path('reports/users/', eventsViews.user_report, name='user_report'),
    path('reports/registrations/', eventsViews.event_report, name='event_report'),
    path('reports/registrations/<int:event_id>/', eventsViews.event_registrations_by_event, name='event_registrations_by_event'),
    path('user_registrations/', eventsViews.user_registered_event, name='user_registered_event'),
    path('reports/registrants/<int:event_id>/', eventsViews.event_registrants, name='event_registrants'),
]

