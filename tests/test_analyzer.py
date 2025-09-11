import pytest

from reminders.analyzer import estimate_task_duration


def test_estimate_short_task():
    assert estimate_task_duration("Quick meeting") == 30


def test_estimate_long_task():
    assert estimate_task_duration("Prepare lengthy annual report") == 8 * 60


def test_estimate_requires_user_input():
    with pytest.warns(UserWarning):
        assert estimate_task_duration("General planning") is None
