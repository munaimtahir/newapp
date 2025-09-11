from datetime import datetime

from .scheduler import determine_reminder_offset


def schedule_reminder(task_due: datetime, expected_minutes: int) -> datetime:
    """Calculate when a reminder should be fired for a task."""
    offset = determine_reminder_offset(expected_minutes)
    return task_due - offset
