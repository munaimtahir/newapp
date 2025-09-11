from datetime import timedelta
from enum import Enum


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
