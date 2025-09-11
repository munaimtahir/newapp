"""
FastAPI server example with spaCy lazy loading and optional preloading.
"""
import os
from fastapi import FastAPI
from pydantic import BaseModel

from app.nlp import get_nlp, preload

app = FastAPI(
    title="spaCy Lazy Loading API",
    description="Example API demonstrating lazy-loaded spaCy models",
    version="1.0.0"
)


class TextRequest(BaseModel):
    text: str


class AnalysisResponse(BaseModel):
    tokens: list[str]
    lemmas: list[str]
    entities: list[dict]
    pos_tags: list[dict]


@app.on_event("startup")
async def startup():
    """
    Startup event handler. Optionally preloads spaCy model if PRELOAD_SPACY=true.
    """
    if os.getenv("PRELOAD_SPACY", "").lower() == "true":
        print("Preloading spaCy model...")
        preload()
        print("spaCy model preloaded successfully!")
    else:
        print("spaCy model will be loaded lazily on first use.")


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "spaCy Lazy Loading API",
        "endpoints": ["/analyze", "/health"],
        "environment": {
            "SPACY_MODEL": os.getenv("SPACY_MODEL", "en_core_web_sm"),
            "SPACY_DISABLE": os.getenv("SPACY_DISABLE", ""),
            "PRELOAD_SPACY": os.getenv("PRELOAD_SPACY", "false")
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: TextRequest):
    """
    Analyze text using the lazy-loaded spaCy model.
    
    Args:
        request: Text analysis request
        
    Returns:
        Analysis results including tokens, lemmas, entities, and POS tags
    """
    nlp = get_nlp()
    doc = nlp(request.text)
    
    return AnalysisResponse(
        tokens=[token.text for token in doc],
        lemmas=[token.lemma_ for token in doc],
        entities=[
            {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
            for ent in doc.ents
        ],
        pos_tags=[
            {"text": token.text, "pos": token.pos_, "tag": token.tag_}
            for token in doc
        ]
    )


@app.get("/analyze")
async def analyze_get(q: str):
    """
    Simple GET endpoint for text analysis.
    
    Args:
        q: Query text to analyze
        
    Returns:
        Simple analysis with tokens only
    """
    nlp = get_nlp()
    doc = nlp(q)
    return {"tokens": [t.text for t in doc]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)