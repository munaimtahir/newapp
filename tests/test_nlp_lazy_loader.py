"""
Tests for the lazy-loading spaCy model accessor.
"""
import os
import threading
import time
from unittest.mock import patch, MagicMock

import pytest

from app.nlp import get_nlp, reset_nlp_for_tests, preload, _get_model_name, _get_disable_components


class TestLazyLoader:
    """Test cases for the lazy loading functionality."""
    
    def setup_method(self):
        """Reset the cached model before each test."""
        reset_nlp_for_tests()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_nlp_for_tests()

    def test_same_instance(self):
        """Test that get_nlp() returns the same instance across multiple calls."""
        reset_nlp_for_tests()
        n1 = get_nlp()
        n2 = get_nlp()
        assert n1 is n2

    def test_pipeline_runs(self):
        """Test that the pipeline processes text correctly."""
        reset_nlp_for_tests()
        nlp = get_nlp()
        doc = nlp("Hello world")
        assert doc is not None
        assert len(doc) > 0
        assert len(list(doc)) == 2  # "Hello" and "world"

    @patch.dict(os.environ, {"SPACY_MODEL": "en_core_web_sm"})
    def test_get_model_name_default(self):
        """Test getting default model name."""
        assert _get_model_name() == "en_core_web_sm"

    @patch.dict(os.environ, {"SPACY_MODEL": "en_core_web_md"})
    def test_get_model_name_custom(self):
        """Test getting custom model name from environment."""
        assert _get_model_name() == "en_core_web_md"

    @patch.dict(os.environ, {}, clear=True)
    def test_get_disable_components_empty(self):
        """Test getting disabled components when none specified."""
        assert _get_disable_components() == []

    @patch.dict(os.environ, {"SPACY_DISABLE": "parser,ner"})
    def test_get_disable_components_multiple(self):
        """Test getting multiple disabled components."""
        components = _get_disable_components()
        assert "parser" in components
        assert "ner" in components
        assert len(components) == 2

    @patch.dict(os.environ, {"SPACY_DISABLE": " parser , ner , "})
    def test_get_disable_components_whitespace(self):
        """Test handling whitespace in disabled components."""
        components = _get_disable_components()
        assert "parser" in components
        assert "ner" in components
        assert len(components) == 2

    def test_preload_functionality(self):
        """Test that preload() loads the model."""
        reset_nlp_for_tests()
        
        # Model should not be loaded initially
        from app.nlp import _NLP
        assert _NLP is None
        
        # Preload should load the model
        preload()
        assert _NLP is not None
        
        # Subsequent calls should return the same instance
        nlp1 = get_nlp()
        nlp2 = get_nlp()
        assert nlp1 is nlp2
        assert nlp1 is _NLP

    def test_thread_safety(self):
        """Test that the lazy loader is thread-safe."""
        reset_nlp_for_tests()
        
        results = []
        
        def load_model():
            nlp = get_nlp()
            results.append(nlp)
        
        # Create multiple threads that try to load the model simultaneously
        threads = [threading.Thread(target=load_model) for _ in range(10)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All threads should get the same instance
        assert len(results) == 10
        first_instance = results[0]
        for instance in results[1:]:
            assert instance is first_instance

    def test_reset_functionality(self):
        """Test that reset_nlp_for_tests() properly resets the cache."""
        # Load model
        nlp1 = get_nlp()
        assert nlp1 is not None
        
        # Reset cache
        reset_nlp_for_tests()
        
        # Loading again should create a new instance
        nlp2 = get_nlp()
        assert nlp2 is not None
        # Note: This might be the same object due to spaCy's internal caching,
        # but the important thing is that our cache was reset
        
        from app.nlp import _NLP
        assert _NLP is nlp2

    @patch('app.nlp.spacy.load')
    def test_model_loading_with_disable(self, mock_load):
        """Test that model loading respects disable parameter."""
        mock_nlp = MagicMock()
        mock_load.return_value = mock_nlp
        
        reset_nlp_for_tests()
        
        with patch.dict(os.environ, {"SPACY_DISABLE": "parser,ner"}):
            nlp = get_nlp()
            
            # Verify spacy.load was called with correct parameters
            mock_load.assert_called_once_with("en_core_web_sm", disable=["parser", "ner"])
            assert nlp is mock_nlp

    @patch('app.nlp.spacy.load')
    def test_model_loading_custom_model(self, mock_load):
        """Test that model loading respects custom model name."""
        mock_nlp = MagicMock()
        mock_load.return_value = mock_nlp
        
        reset_nlp_for_tests()
        
        with patch.dict(os.environ, {"SPACY_MODEL": "en_core_web_lg"}):
            nlp = get_nlp()
            
            # Verify spacy.load was called with custom model
            mock_load.assert_called_once_with("en_core_web_lg", disable=[])
            assert nlp is mock_nlp

    def test_basic_nlp_functionality(self):
        """Test basic NLP functionality works as expected."""
        nlp = get_nlp()
        
        # Test text processing
        text = "Apple Inc. is looking at buying U.K. startup for $1 billion"
        doc = nlp(text)
        
        # Check that we get tokens
        tokens = [token.text for token in doc]
        assert len(tokens) > 0
        assert "Apple" in tokens
        assert "Inc." in tokens
        
        # Check that we can get lemmas
        lemmas = [token.lemma_ for token in doc]
        assert len(lemmas) == len(tokens)
        
        # Check that we can get POS tags
        pos_tags = [token.pos_ for token in doc]
        assert len(pos_tags) == len(tokens)


class TestIntegration:
    """Integration tests using the actual spaCy model."""
    
    def setup_method(self):
        """Reset the cached model before each test."""
        reset_nlp_for_tests()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_nlp_for_tests()

    def test_real_model_loading(self):
        """Test loading the actual spaCy model (requires model to be installed)."""
        try:
            nlp = get_nlp()
            doc = nlp("This is a test sentence.")
            
            # Should have tokens
            assert len(doc) == 5  # "This", "is", "a", "test", "sentence", "."
            
            # Should be able to iterate over tokens
            tokens = list(doc)
            assert len(tokens) == 5
            
            # Tokens should have expected attributes
            for token in tokens:
                assert hasattr(token, 'text')
                assert hasattr(token, 'lemma_')
                assert hasattr(token, 'pos_')
                
        except OSError:
            # Model not installed, skip test
            pytest.skip("spaCy model not installed")

    def test_performance_benefit(self):
        """Test that lazy loading provides performance benefits."""
        import time
        
        # Time how long it takes to import the module
        start_time = time.time()
        from app import nlp  # This should be fast as no model is loaded
        import_time = time.time() - start_time
        
        # Import should be very fast (under 1 second)
        assert import_time < 1.0
        
        # First call to get_nlp() will load the model (should be slower)
        start_time = time.time()
        try:
            nlp_instance = nlp.get_nlp()
            first_load_time = time.time() - start_time
            
            # Second call should be much faster (cached)
            start_time = time.time()
            nlp_instance2 = nlp.get_nlp()
            cached_load_time = time.time() - start_time
            
            # Cached access should be much faster
            assert cached_load_time < first_load_time / 10  # At least 10x faster
            assert nlp_instance is nlp_instance2
            
        except OSError:
            # Model not installed, skip test
            pytest.skip("spaCy model not installed")