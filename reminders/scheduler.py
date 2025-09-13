from datetime import datetime, time, timedelta
from enum import Enum
from typing import List


class DurationCategory(Enum):
    """Represent expected task duration buckets."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


CATEGORY_OFFSETS = {
    DurationCategory.SHORT: timedelta(minutes=10),
    DurationCategory.MEDIUM: timedelta(hours=1),
    DurationCategory.LONG: timedelta(days=1),
}


def determine_reminder_offset(expected_minutes: int) -> timedelta:
    """Return a lead time for reminders based on expected duration.

    Parameters
    ----------
    expected_minutes:
        The anticipated duration of the task in minutes.

    Returns
    -------
    timedelta
        The amount of time before the scheduled task when the reminder should
        trigger.
    """

    if expected_minutes < 60:
        category = DurationCategory.SHORT
    elif expected_minutes <= 8 * 60:  # 1-8 hours inclusive
        category = DurationCategory.MEDIUM
    else:
        category = DurationCategory.LONG

    return CATEGORY_OFFSETS[category]


class PrepCategory(Enum):
    """Buckets describing how much preparation time a task requires."""

    UNDER_FOUR_HOURS = "under_four_hours"
    ONE_DAY = "one_day"
    FEW_DAYS = "few_days"
    LONG_TERM = "long_term"


def categorize_prep_time(prep_minutes: int) -> PrepCategory:
    """Categorize a task based on the estimated preparation time."""

    if prep_minutes < 4 * 60:
        return PrepCategory.UNDER_FOUR_HOURS
    if prep_minutes < 24 * 60:
        return PrepCategory.ONE_DAY
    if prep_minutes < 7 * 24 * 60:
        return PrepCategory.FEW_DAYS
    return PrepCategory.LONG_TERM


def _start_of_week(dt: datetime, hour: int) -> datetime:
    week_start_date = dt.date() - timedelta(days=dt.weekday())
    return datetime.combine(week_start_date, time(hour=hour, minute=0))


def generate_reminder_schedule(task_due: datetime, prep_minutes: int) -> List[datetime]:
    """Generate reminder datetimes according to preparation category."""

    category = categorize_prep_time(prep_minutes)
    reminders: List[datetime] = []
    due_date = task_due.date()

    if category == PrepCategory.UNDER_FOUR_HOURS:
        reminders.append(task_due - timedelta(hours=4))
        reminders.append(datetime.combine(due_date - timedelta(days=1), time(8, 0)))
        reminders.append(datetime.combine(due_date, time(8, 0)))

    elif category == PrepCategory.ONE_DAY:
        reminders.append(task_due - timedelta(days=1))
        start = _start_of_week(task_due, 7)
        day = start
        while day.date() <= due_date:
            reminders.append(day)
            day += timedelta(days=1)

    elif category == PrepCategory.FEW_DAYS:
        start_week = _start_of_week(task_due, 8)
        reminders.append(start_week)
        day = start_week + timedelta(days=1)
        while day.date() <= due_date:
            reminders.append(datetime.combine(day.date(), time(7, 0)))
            day += timedelta(days=1)

    else:  # LONG_TERM
        month_before = datetime.combine(due_date - timedelta(days=30), time(7, 0))
        reminders.append(month_before)

        week_start = _start_of_week(task_due, 7)
        current = month_before + timedelta(days=(7 - month_before.weekday()) % 7)
        while current < week_start:
            reminders.append(current.replace(hour=7, minute=0, second=0, microsecond=0))
            current += timedelta(days=7)

        day = week_start
        while day.date() <= due_date:
            reminders.append(day)
            day += timedelta(days=1)

    # Remove duplicates and sort
    unique = sorted(set(reminders))
    return unique
