from datetime import datetime

from reminders.parser import parse_reminder_text


def test_parse_reminder_text_basic():
    due, task, duration = parse_reminder_text("Finish report on 2024-01-05 at 09:30")
    assert due == datetime(2024, 1, 5, 9, 30)
    assert task == "Finish report"
    assert duration is None

