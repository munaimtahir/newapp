"""
Lazy-loading, cached spaCy model accessor.

Environment:
- SPACY_MODEL: Name of the spaCy model to load (default: "en_core_web_sm")
- SPACY_DISABLE: Comma-separated pipeline components to disable (e.g., "parser,ner")
- PRELOAD_SPACY: If "true", you can call preload() at app startup to warm the cache.
"""
from __future__ import annotations

import os
from threading import Lock
from typing import Optional

import spacy

_lock = Lock()
_NLP = None  # type: Optional["spacy.language.Language"]


def _get_model_name() -> str:
    return os.getenv("SPACY_MODEL", "en_core_web_sm")


def _get_disable_components() -> list[str]:
    raw = os.getenv("SPACY_DISABLE", "").strip()
    if not raw:
        return []
    return [c.strip() for c in raw.split(",") if c.strip()]


def get_nlp():
    """
    Returns a cached spaCy Language instance, loading it on first use.
    Thread-safe, process-local singleton.
    """
    global _NLP
    if _NLP is None:
        with _lock:
            if _NLP is None:
                model_name = _get_model_name()
                disable = _get_disable_components()
                # Load lazily and cache
                nlp = spacy.load(model_name, disable=disable)
                _NLP = nlp
    return _NLP


def preload():
    """
    Optionally call this at application startup if you want to warm the cache.
    No-op if already loaded.
    """
    _ = get_nlp()


def reset_nlp_for_tests():
    """
    Testing helper to reset the cached model between tests or when changing SPACY_MODEL.
    """
    global _NLP
    with _lock:
        _NLP = None