from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from typing import Optional

from dateparser.search import search_dates


@dataclass
class ParsedReminder:
    """Structured representation of a parsed reminder."""

    description: str
    when: datetime
    duration: Optional[timedelta] = None


def parse_reminder_text(text: str) -> ParsedReminder:
    """Parse a natural language reminder string.

    Parameters
    ----------
    text:
        Freeform reminder text such as "Pay rent tomorrow at 3pm for 2 hours".

    Returns
    -------
    ParsedReminder
        Structured details about the reminder.

    Raises
    ------
    ValueError
        If either a date/time or description could not be determined.
    """

    if not text or not text.strip():
        raise ValueError("No reminder text provided")

    # Identify date/time expressions within the text.
    results = search_dates(text, settings={"PREFER_DATES_FROM": "future"})
    if not results:
        raise ValueError("Could not parse a date or time from the reminder")

    match_text, when = results[0]

    # Extract optional duration phrases like "for 2 hours".
    duration_pattern = re.compile(
        r"for\s+(?:(\d+)\s*(minutes?|hours?|days?)|an?\s*(hour|minute|day))",
        re.IGNORECASE,
    )
    duration_match = duration_pattern.search(text)
    duration: Optional[timedelta] = None
    if duration_match:
        if duration_match.group(1):
            amount = int(duration_match.group(1))
            unit = duration_match.group(2).lower()
        else:
            amount = 1
            unit = duration_match.group(3).lower()
        if unit.startswith("minute"):
            duration = timedelta(minutes=amount)
        elif unit.startswith("hour"):
            duration = timedelta(hours=amount)
        elif unit.startswith("day"):
            duration = timedelta(days=amount)

    # Remove the detected date/time and duration text to obtain the description.
    description = text
    description = description.replace(match_text, "")
    if duration_match:
        description = duration_pattern.sub("", description)
    description = re.sub(r"\s+", " ", description).strip(", .")

    if not description:
        raise ValueError("Could not determine the task description")

    return ParsedReminder(description=description, when=when, duration=duration)
