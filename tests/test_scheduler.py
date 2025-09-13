from datetime import datetime, timedelta

import pytest

from reminders.scheduler import (
    determine_reminder_offset,
    generate_reminder_schedule,
)
from reminders.service import schedule_reminder


def test_short_category():
    assert determine_reminder_offset(0) == timedelta(minutes=10)
    assert determine_reminder_offset(59) == timedelta(minutes=10)


def test_medium_category_boundaries():
    assert determine_reminder_offset(60) == timedelta(hours=1)
    assert determine_reminder_offset(8 * 60) == timedelta(hours=1)


def test_long_category():
    assert determine_reminder_offset(8 * 60 + 1) == timedelta(days=1)


def test_schedule_reminder_integration():
    due = datetime(2024, 1, 1, 12, 0)
    reminder = schedule_reminder(due, 30)
    assert reminder == due - timedelta(minutes=10)


def test_generate_schedule_under_four_hours():
    due = datetime(2024, 1, 2, 13, 0)
    schedule = generate_reminder_schedule(due, 60)
    assert schedule == [
        datetime(2024, 1, 1, 8, 0),
        datetime(2024, 1, 2, 8, 0),
        datetime(2024, 1, 2, 9, 0),
    ]


def test_generate_schedule_long_term():
    due = datetime(2024, 2, 14, 10, 0)
    schedule = generate_reminder_schedule(due, 8 * 24 * 60)
    assert datetime(2024, 1, 15, 7, 0) in schedule
    assert datetime(2024, 2, 12, 7, 0) in schedule
    assert datetime(2024, 2, 14, 7, 0) in schedule
