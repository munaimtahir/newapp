"""Tools for estimating task durations from descriptions."""
from __future__ import annotations

from typing import Optional
import warnings

# Mapping of keywords to their estimated durations in minutes.
_KEYWORD_ESTIMATES = {
    "short": 30,
    "quick": 30,
    "brief": 30,
    "long": 8 * 60,
    "lengthy": 8 * 60,
    "complex": 8 * 60,
}


def estimate_task_duration(description: str) -> Optional[int]:
    """Estimate the expected duration of a task in minutes.

    The function applies a few simple keyword-based heuristics. If no keyword is
    detected, the function returns ``None`` and emits a :class:`UserWarning` to
    indicate that explicit user input is required.

    Parameters
    ----------
    description:
        Natural language description of the task.

    Returns
    -------
    Optional[int]
        The estimated number of minutes for the task, or ``None`` if the
        description is insufficient for inference.
    """

    desc = description.lower()
    for keyword, minutes in _KEYWORD_ESTIMATES.items():
        if keyword in desc:
            return minutes

    warnings.warn(
        "Unable to estimate duration from description; user input is required.",
        UserWarning,
    )
    return None
