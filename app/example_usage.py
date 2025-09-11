"""
Example usage of the lazy-loading spaCy model accessor.
"""
from app.nlp import get_nlp


def analyze_text(text: str):
    """
    Analyze text using the lazy-loaded spaCy model.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of lemmatized tokens
    """
    nlp = get_nlp()
    doc = nlp(text)
    return [token.lemma_ for token in doc]


def extract_entities(text: str):
    """
    Extract named entities from text using the lazy-loaded spaCy model.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of entities with their labels
    """
    nlp = get_nlp()
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def get_pos_tags(text: str):
    """
    Get part-of-speech tags from text using the lazy-loaded spaCy model.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of (token, pos_tag) tuples
    """
    nlp = get_nlp()
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]


if __name__ == "__main__":
    # Example usage
    sample_text = "Apple Inc. is looking at buying U.K. startup for $1 billion"
    
    print("Sample text:", sample_text)
    print("\nLemmas:", analyze_text(sample_text))
    print("Entities:", extract_entities(sample_text))
    print("POS tags:", get_pos_tags(sample_text))