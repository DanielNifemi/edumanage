from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Schedule, Event
from .forms import ScheduleForm, EventForm
from teachers.models import Class


@login_required
def class_schedule(request, class_id):
    class_group = get_object_or_404(Class, id=class_id)
    schedules = Schedule.objects.filter(class_group=class_group).order_by('day', 'time_slot')
    return render(request, 'schedules/class_schedule.html', {'class_group': class_group, 'schedules': schedules})


@login_required
def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_schedule', class_id=form.cleaned_data['class_group'].id)
    else:
        form = ScheduleForm()
    return render(request, 'schedules/add_schedule.html', {'form': form})


@login_required
def event_list(request):
    events = Event.objects.all().order_by('start_datetime')
    return render(request, 'schedules/event_list.html', {'events': events})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'schedules/add_event.html', {'form': form})
