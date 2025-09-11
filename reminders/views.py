from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ReminderForm
from .models import Reminder
from .parsers import parse_reminder


def index(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            tz = str(timezone.get_current_timezone())
            dt, location = parse_reminder(text, tz)
            if dt:
                Reminder.objects.create(
                    original_text=text, parsed_time=dt, location=location
                )
                return redirect("reminders:index")
    else:
        form = ReminderForm()
    reminders = Reminder.objects.order_by("-created_at")[:10]
    return render(
        request,
        "reminders/index.html",
        {"form": form, "reminders": reminders},
    )
