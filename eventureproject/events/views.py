from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Events, Users, Group
from .forms import EventForm

# Check if the user is administrator
def is_admin(user):
    return hasattr(user, 'users') and user.users.group.group_name == 'administrator'

# Check if the user is registrant
def is_registrant(user):
    return hasattr(user, 'users') and user.users.group.group_name == 'registrant'

# Only allow access to logged-in users
@login_required
def events(request):
    current_user = request.user.users
    # Get all events from the database, sorted by starting date
    all_events = Events.objects.all().order_by('start_date')
    # Get a list of event IDs that this user has registered for
    registered_event_ids = current_user.registered_events.values_list('id', flat=True)
    return render(request, 'events.html', {
        'events': all_events, # All events to display
        'registrations': registered_event_ids, # Events the user is registered in
        'is_admin': is_admin(request.user), # check if the user is an admin
        'name': request.user.first_name or request.user.username, # Show user’s name else show username
    })


@login_required
def create_event(request):
    # If not admin, redirect to event page
    if not is_admin(request.user):
        return redirect('events')

    if request.method == 'POST':
        # Create form with submitted data
        form = EventForm(request.POST)
        if form.is_valid():
            # Save the new event to the database
            form.save()
            #  After saving, go back to event page
            return redirect('events')
    else:
        form = EventForm()
        # If not posting, just show an empty form
    return render(request, 'create_event.html', {'form': form})


# view to delete an event
@login_required
def delete_event(request, event_id):
    # Only admins can delete  else redirect to events page
    if not is_admin(request.user):
        return redirect('events')

    # Get the event by ID or return a error if not found using django built in shortcut
    event = get_object_or_404(Events, id=event_id)
    # Delete the event from the database
    event.delete()
    # After deletion, go back to the event page
    return redirect('events')

# view to see a event in a page
@login_required
def event_view(request, event_id):
    event = get_object_or_404(Events, id=event_id)
     # Get the custom user model
    current_user = request.user.users
    # Check if edit is clicked is requested
    is_edit = request.GET.get('edit') == 'true'
    # Check if the current user is registered for this event
    is_registered = event.users.filter(id=current_user.id).exists()


    # view for admin
    if is_admin(request.user):
        if is_edit:
            if request.method == 'POST':
                 # Form to update existing event
                form = EventForm(request.POST, instance=event)
                if form.is_valid():
                    # Save the updated event
                    form.save()
                    return redirect('events')
            else:
                form = EventForm(instance=event)
            return render(request, 'event_view.html', {
                'event': event,
                'form': form,
                'is_edit': True
            })
        return render(request, 'event_view.html', {
            'event': event,
            'is_edit': False
        })

    if is_registrant(request.user):
        if not is_registered:
            return redirect('events')
        return render(request, 'event_view.html', {
            'event': event,
            'is_registered': True,
            'is_edit': False
        })

# view to register from an event
@login_required
def register(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    current_user = request.user.users
    event.users.add(current_user)
    return redirect('event_view', event_id=event.id)

# view to unregister from an event
@login_required
def unregister(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    current_user = request.user.users
    event.users.remove(current_user)
    return redirect('events')

# User Report - View a list of all registered users
@login_required
def user_report(request):
    if not is_admin(request.user):
        return redirect('events')

    all_users = Users.objects.all()
    return render(request, 'user_report.html', {'users': all_users})


# Event Report - View all events and their registrants
@login_required
def event_report(request):
    if not is_admin(request.user):
        return redirect('events')

    events = Events.objects.prefetch_related('users__user').all()
    return render(request, 'event_report.html', {
        'is_admin': True,
        'events': events
    })


# Event Report - View all users registered for a specific event
@login_required
def event_registrations_by_event(request, event_id):
    if not is_admin(request.user):
        return redirect('events')

    event = get_object_or_404(Events, id=event_id)
    return render(request, 'event_single_report.html', {
        'event': event,
        'registrations': event.users.all()
    })

# View to show the  registered events
@login_required
def user_registered_event(request):
    if not is_registrant(request.user):
        return redirect('events')

    user = request.user.users
    events = user.registered_events.all()
    return render(request, 'user_registered_event.html', {'events': events})

#  Event Report - View all users who registered for each event
@login_required
def event_registrants(request, event_id):
    if not is_admin(request.user):
        return redirect('events')
     # Get all users registered to this event
    event = get_object_or_404(Events, id=event_id)
    registrations = event.users.all()
    return render(request, 'event_registrants.html', {
        'event': event,
        'registrations': registrations,
    })