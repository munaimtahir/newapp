from datetime import datetime, timedelta

import pytest

from reminders.parser import ParsedReminder, parse_reminder_text


def test_parse_reminder_with_duration():
    text = "Finish report July 5, 2030 at 3pm for 2 hours"
    parsed = parse_reminder_text(text)
    assert parsed.description == "Finish report"
    assert parsed.when == datetime(2030, 7, 5, 15, 0)
    assert parsed.duration == timedelta(hours=2)


def test_parse_reminder_missing_datetime_raises():
    with pytest.raises(ValueError):
        parse_reminder_text("Finish report soon")


def test_parse_reminder_natural_language():
    now = datetime.now()
    parsed = parse_reminder_text("Call mom tomorrow at 3pm")
    expected = (now + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)
    assert parsed.description == "Call mom"
    assert parsed.when.year == expected.year
    assert parsed.when.month == expected.month
    assert parsed.when.day == expected.day
    assert parsed.when.hour == 15
    assert parsed.when.minute == 0
