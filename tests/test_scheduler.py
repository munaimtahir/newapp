from datetime import datetime, timedelta

import pytest

from reminders.scheduler import determine_reminder_offset
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
