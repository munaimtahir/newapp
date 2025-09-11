from datetime import datetime

import pytest

from reminders.service import create_reminder_from_text


def test_create_reminder_with_parsed_duration(monkeypatch):
    due = datetime(2024, 1, 1, 12, 0)

    def fake_parse(text: str):
        assert text == "take out trash at noon"
        return due, "take out trash", 30

    def fake_schedule(task_due, expected_minutes):
        assert task_due == due
        assert expected_minutes == 30
        return datetime(2024, 1, 1, 11, 50)

    monkeypatch.setattr("reminders.service.parse_reminder_text", fake_parse, raising=False)
    monkeypatch.setattr("reminders.service.schedule_reminder", fake_schedule)

    reminder = create_reminder_from_text("take out trash at noon")
    assert reminder == datetime(2024, 1, 1, 11, 50)


def test_create_reminder_ai_estimation(monkeypatch):
    due = datetime(2024, 2, 1, 9, 0)

    def fake_parse(text: str):
        return due, "write report", None

    def fake_estimate(description: str):
        assert description == "write report"
        return 45

    def fake_schedule(task_due, expected_minutes):
        assert task_due == due
        assert expected_minutes == 45
        return datetime(2024, 2, 1, 8, 15)

    monkeypatch.setattr("reminders.service.parse_reminder_text", fake_parse, raising=False)
    monkeypatch.setattr("reminders.service.estimate_task_duration", fake_estimate, raising=False)
    monkeypatch.setattr("reminders.service.schedule_reminder", fake_schedule)

    reminder = create_reminder_from_text("write a report by 9am")
    assert reminder == datetime(2024, 2, 1, 8, 15)


def test_create_reminder_needs_user_clarification(monkeypatch):
    due = datetime(2024, 3, 1, 10, 0)

    def fake_parse(text: str):
        return due, "mystery task", None

    def fake_estimate(description: str):
        return None

    monkeypatch.setattr("reminders.service.parse_reminder_text", fake_parse, raising=False)
    monkeypatch.setattr("reminders.service.estimate_task_duration", fake_estimate, raising=False)

    with pytest.raises(ValueError):
        create_reminder_from_text("some task")

