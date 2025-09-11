import dateparser
import spacy

nlp = spacy.load("en_core_web_sm")


def parse_reminder(text: str, tz: str = "UTC"):
    """Return (datetime, location) parsed from free-form text."""
    parsed_date = dateparser.parse(
        text,
        settings={"TIMEZONE": tz, "RETURN_AS_TIMEZONE_AWARE": True},
    )
    doc = nlp(text)
    places = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC", "FAC", "ORG")]
    location = places[0] if places else ""
    return parsed_date, location
