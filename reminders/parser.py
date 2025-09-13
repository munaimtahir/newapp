import re
from datetime import datetime
from typing import Tuple, Optional


def parse_reminder_text(text: str) -> Tuple[datetime, str, Optional[int]]:
    """Parse a free-form reminder description.

    The expected format is ``"<task> on YYYY-MM-DD at HH:MM"``. The function
    returns the due datetime for the task, the task description, and any
    specified duration in minutes if present. If no duration is detected, the
    third item in the tuple is ``None``.
    """
    pattern = r"(?P<task>.+?)\s+on\s+(?P<date>\d{4}-\d{2}-\d{2})\s+at\s+(?P<time>\d{1,2}:\d{2})"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        raise ValueError("Unable to parse reminder text")

    task = match.group("task").strip()
    date_str = match.group("date")
    time_str = match.group("time")
    due = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

    # Basic duration extraction: look for patterns like 'for Xh' or 'for Xm'
    duration_match = re.search(r"for\s+(?P<value>\d+)\s*(?P<unit>[hm])", text, re.IGNORECASE)
    expected_minutes: Optional[int]
    if duration_match:
        value = int(duration_match.group("value"))
        unit = duration_match.group("unit").lower()
        expected_minutes = value * 60 if unit == "h" else value
    else:
        expected_minutes = None

    return due, task, expected_minutes
