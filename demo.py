#!/usr/bin/env python3
"""
Command-line interface for demonstrating spaCy lazy loading.
"""
import argparse
import time
from app.nlp import get_nlp, preload, reset_nlp_for_tests


def main():
    parser = argparse.ArgumentParser(description="spaCy Lazy Loading Demo")
    parser.add_argument("text", nargs="?", help="Text to analyze")
    parser.add_argument("--preload", action="store_true", help="Preload the model")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmark")
    parser.add_argument("--reset", action="store_true", help="Reset cached model")
    
    args = parser.parse_args()
    
    if args.reset:
        print("Resetting cached model...")
        reset_nlp_for_tests()
        print("Model cache cleared.")
        return
    
    if args.preload:
        print("Preloading spaCy model...")
        start_time = time.time()
        preload()
        load_time = time.time() - start_time
        print(f"Model preloaded in {load_time:.3f} seconds")
        return
    
    if args.benchmark:
        run_benchmark()
        return
    
    if not args.text:
        args.text = input("Enter text to analyze: ")
    
    analyze_text(args.text)


def analyze_text(text):
    """Analyze the given text and display results."""
    print(f"\nAnalyzing: '{text}'")
    print("-" * 50)
    
    # Time the first call (may include model loading)
    start_time = time.time()
    nlp = get_nlp()
    doc = nlp(text)
    analysis_time = time.time() - start_time
    
    print(f"Analysis time: {analysis_time:.3f} seconds")
    print()
    
    # Display tokens and their properties
    print("Tokens:")
    for token in doc:
        print(f"  {token.text:<15} | Lemma: {token.lemma_:<15} | POS: {token.pos_:<10} | Tag: {token.tag_}")
    
    # Display entities if any
    if doc.ents:
        print("\nEntities:")
        for ent in doc.ents:
            print(f"  {ent.text:<20} | Label: {ent.label_:<10} | Description: {spacy.explain(ent.label_)}")
    
    # Display sentences
    print(f"\nSentences ({len(list(doc.sents))}):")
    for i, sent in enumerate(doc.sents, 1):
        print(f"  {i}. {sent.text}")


def run_benchmark():
    """Run performance benchmarks."""
    print("Running performance benchmark...")
    print("=" * 60)
    
    # Test 1: Import time (should be fast)
    start_time = time.time()
    from app import nlp
    import_time = time.time() - start_time
    print(f"Import time: {import_time:.6f} seconds")
    
    # Reset to ensure clean test
    reset_nlp_for_tests()
    
    # Test 2: First model access (includes loading)
    start_time = time.time()
    nlp_instance = get_nlp()
    first_load_time = time.time() - start_time
    print(f"First model load: {first_load_time:.3f} seconds")
    
    # Test 3: Subsequent access (cached)
    start_time = time.time()
    nlp_instance2 = get_nlp()
    cached_access_time = time.time() - start_time
    print(f"Cached access: {cached_access_time:.6f} seconds")
    
    # Verify same instance
    print(f"Same instance: {nlp_instance is nlp_instance2}")
    
    # Test 4: Text processing performance
    test_text = "Apple Inc. is looking at buying U.K. startup for $1 billion"
    start_time = time.time()
    doc = nlp_instance(test_text)
    processing_time = time.time() - start_time
    print(f"Text processing: {processing_time:.6f} seconds")
    
    print("\nPerformance Summary:")
    print(f"  Speedup factor: {first_load_time / cached_access_time:.0f}x faster for cached access")
    print(f"  Tokens processed: {len(doc)}")
    print(f"  Processing rate: {len(doc) / processing_time:.0f} tokens/second")


if __name__ == "__main__":
    import spacy
    main()