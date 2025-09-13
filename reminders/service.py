from datetime import datetime
from typing import List

from .analyzer import estimate_task_duration
from .parser import parse_reminder_text
from .scheduler import determine_reminder_offset, generate_reminder_schedule


def schedule_reminder(task_due: datetime, expected_minutes: int) -> datetime:
    """Calculate when a reminder should be fired for a task."""
    offset = determine_reminder_offset(expected_minutes)
    return task_due - offset


def schedule_reminders(task_due: datetime, expected_minutes: int) -> List[datetime]:
    """Return a series of reminder datetimes for the task.

    The reminder series is determined by the expected preparation duration of
    the task. See :func:`generate_reminder_schedule` for the exact rules.
    """

    return generate_reminder_schedule(task_due, expected_minutes)


def create_reminder_from_text(text: str) -> List[datetime]:
    """Create and schedule a reminder based on a free-form description.

    The ``text`` is parsed via :func:`parse_reminder_text` to determine when the
    task is due, what the task description is, and optionally how long the task
    is expected to take. If the parser cannot determine a duration, an AI based
    estimation is attempted via :func:`estimate_task_duration`. If that also
    fails to provide an estimate, callers are expected to ask the user for
    clarification and a :class:`ValueError` is raised.

    The resolved values are then passed to :func:`schedule_reminder` to
    determine the actual reminder time.
    """

    task_due, description, expected_minutes = parse_reminder_text(text)

    if expected_minutes is None:
        expected_minutes = estimate_task_duration(description)
        if expected_minutes is None:
            raise ValueError("Unable to determine task duration; ask the user.")

    return schedule_reminders(task_due, expected_minutes)
