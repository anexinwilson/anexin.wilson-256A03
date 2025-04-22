from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Events, Users, Group
from .forms import EventForm


def is_admin(user):
    return hasattr(user, 'users') and user.users.group.group_name == 'administrator'


def is_registrant(user):
    return hasattr(user, 'users') and user.users.group.group_name == 'registrant'


@login_required
def events(request):
    current_user = request.user.users
    all_events = Events.objects.all().order_by('start_date')
    registered_event_ids = current_user.registered_events.values_list('id', flat=True)
    return render(request, 'events.html', {
        'events': all_events,
        'registrations': registered_event_ids,
        'is_admin': is_admin(request.user),
        'name': request.user.first_name or request.user.username,
    })


@login_required
def create_event(request):
    if not is_admin(request.user):
        return redirect('events')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def delete_event(request, event_id):
    if not is_admin(request.user):
        return redirect('events')

    event = get_object_or_404(Events, id=event_id)
    event.delete()
    return redirect('events')


@login_required
def event_view(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    current_user = request.user.users
    is_edit = request.GET.get('edit') == 'true'
    is_registered = event.users.filter(id=current_user.id).exists()

    if is_admin(request.user):
        if is_edit:
            if request.method == 'POST':
                form = EventForm(request.POST, instance=event)
                if form.is_valid():
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


@login_required
def register(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    current_user = request.user.users
    event.users.add(current_user)
    return redirect('event_view', event_id=event.id)


@login_required
def unregister(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    current_user = request.user.users
    event.users.remove(current_user)
    return redirect('events')


@login_required
def user_report(request):
    if not is_admin(request.user):
        return redirect('events')

    all_users = Users.objects.all()
    return render(request, 'user_report.html', {'users': all_users})


@login_required
def event_report(request):
    if not is_admin(request.user):
        return redirect('events')

    events = Events.objects.prefetch_related('users__user').all()
    return render(request, 'event_report.html', {
        'is_admin': True,
        'events': events
    })


@login_required
def event_registrations_by_event(request, event_id):
    if not is_admin(request.user):
        return redirect('events')

    event = get_object_or_404(Events, id=event_id)
    return render(request, 'event_single_report.html', {
        'event': event,
        'registrations': event.users.all()
    })


@login_required
def user_registered_event(request):
    if not is_registrant(request.user):
        return redirect('events')

    user = request.user.users
    events = user.registered_events.all()
    return render(request, 'user_registered_event.html', {'events': events})

@login_required
def event_registrants(request, event_id):
    if not is_admin(request.user):
        return redirect('events')

    event = get_object_or_404(Events, id=event_id)
    registrations = event.users.all()
    return render(request, 'event_registrants.html', {
        'event': event,
        'registrations': registrations,
    })