# newapp

A modern Python application demonstrating lazy-loading, cached spaCy model access for improved startup performance and memory efficiency.

## Features

- **Lazy Loading**: spaCy models are loaded only when first needed, not at import time
- **Thread-Safe Caching**: Single model instance shared across all threads in a process
- **Environment Configuration**: Flexible model and pipeline configuration via environment variables
- **Optional Preloading**: Warm-start capability for production deployments
- **FastAPI Integration**: Example web API with startup hooks and async endpoints

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/munaimtahir/newapp.git
cd newapp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the default spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Basic Usage

```python
from app.nlp import get_nlp

# Model loads lazily on first use
nlp = get_nlp()
doc = nlp("Hello world!")
print([token.lemma_ for token in doc])
```

### Running the FastAPI Server

```bash
# Start the server
python app/server.py

# Or with uvicorn
uvicorn app.server:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API documentation.

## Environment Variables

Configure the spaCy model loading behavior using these environment variables:

### `SPACY_MODEL`
**Default**: `en_core_web_sm`

Specifies which spaCy model to load. Any installed spaCy model can be used.

```bash
export SPACY_MODEL=en_core_web_md
export SPACY_MODEL=en_core_web_lg
export SPACY_MODEL=de_core_news_sm  # German model
```

### `SPACY_DISABLE`
**Default**: *(empty)*

Comma-separated list of pipeline components to disable for better performance and reduced memory usage.

```bash
# Disable parser and NER for faster processing
export SPACY_DISABLE=parser,ner

# Disable multiple components
export SPACY_DISABLE=parser,ner,lemmatizer
```

Common components you might want to disable:
- `tagger` - Part-of-speech tagging
- `parser` - Dependency parsing
- `ner` - Named entity recognition
- `lemmatizer` - Lemmatization
- `textcat` - Text classification

### `PRELOAD_SPACY`
**Default**: `false`

When set to `true`, the spaCy model will be preloaded during application startup instead of on first use.

```bash
export PRELOAD_SPACY=true
```

**Use cases for preloading:**
- Production deployments where you want predictable response times
- Applications with strict SLA requirements
- When you know the model will be needed immediately

## API Usage Examples

### Analyze Text
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Apple Inc. is looking at buying U.K. startup for $1 billion"}'
```

### Simple Analysis (GET)
```bash
curl "http://localhost:8000/analyze?q=Hello%20world"
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

## Performance Benefits

### Import Performance
```python
# ❌ Traditional approach - blocks import
import spacy
nlp = spacy.load("en_core_web_sm")  # ~2-5 seconds

# ✅ Lazy loading approach - fast import
from app.nlp import get_nlp  # ~0.01 seconds
# Model loads only when needed:
nlp = get_nlp()  # ~2-5 seconds on first call, ~0.001 seconds thereafter
```

### Memory Efficiency
- **Single Instance**: One model per process, shared across all threads
- **Conditional Loading**: Models only loaded if actually used
- **Component Disabling**: Reduce memory footprint by disabling unused components

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_nlp_lazy_loader.py

# Run with coverage
pytest --cov=app tests/
```

### Test Categories

1. **Unit Tests**: Test the lazy loading mechanism, caching, and configuration
2. **Integration Tests**: Test with actual spaCy models
3. **Thread Safety Tests**: Verify thread-safe singleton behavior
4. **Performance Tests**: Validate performance improvements

## Architecture

### Core Components

- **`app/nlp.py`**: Lazy-loading spaCy model accessor with caching
- **`app/example_usage.py`**: Example functions demonstrating usage patterns
- **`app/server.py`**: FastAPI server with lazy loading integration
- **`tests/test_nlp_lazy_loader.py`**: Comprehensive test suite

### Design Patterns

1. **Singleton Pattern**: Single model instance per process
2. **Lazy Initialization**: Deferred loading until first use
3. **Double-Checked Locking**: Thread-safe initialization
4. **Environment-Based Configuration**: Runtime configuration via env vars

## Best Practices

### For Library Authors
```python
# ❌ Don't load models at import time
import spacy
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    return nlp(text)

# ✅ Use lazy loading
from app.nlp import get_nlp

def process_text(text):
    nlp = get_nlp()
    return nlp(text)
```

### For Application Developers
```python
# For long-running processes, cache the reference
class TextProcessor:
    def __init__(self):
        self._nlp = None
    
    @property
    def nlp(self):
        if self._nlp is None:
            self._nlp = get_nlp()
        return self._nlp
    
    def process(self, text):
        return self.nlp(text)
```

### For Production Deployments
```bash
# Set environment variables for optimal performance
export SPACY_MODEL=en_core_web_sm
export SPACY_DISABLE=parser,ner  # If you don't need parsing/NER
export PRELOAD_SPACY=true        # For predictable startup
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.