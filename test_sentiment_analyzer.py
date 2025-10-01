"""
Unit tests for sentiment analyzer
Run with: pytest test_sentiment_analyzer.py
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentiment_analyzer import load_data_file


class TestDataLoading:
    """Test data loading functionality"""
    
    def test_load_csv_file(self, tmp_path):
        """Test loading CSV file"""
        # Create temporary CSV file
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("review_id,text\n1,Great product\n2,Bad quality")
        
        df = load_data_file(str(csv_file))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'review_id' in df.columns
        assert 'text' in df.columns
    
    def test_load_invalid_file_type(self, tmp_path):
        """Test that invalid file type raises error"""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("some text")
        
        with pytest.raises(ValueError, match="File must be CSV or XLSX format"):
            load_data_file(str(txt_file))


class TestSentimentAnalyzer:
    """Test sentiment analyzer functionality"""
    
    @patch('sentiment_analyzer.pipeline')
    def test_analyze_empty_text(self, mock_pipeline):
        """Test that empty text returns neutral sentiment"""
        from sentiment_analyzer import SentimentAnalyzer
        
        # Mock the pipeline
        mock_pipeline.return_value = Mock()
        
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text("")
        
        assert result['sentiment'] == 'neutral'
        assert result['confidence'] == 0.0
        assert result['stars'] == 3
    
    @patch('sentiment_analyzer.pipeline')
    def test_analyze_none_text(self, mock_pipeline):
        """Test that None text returns neutral sentiment"""
        from sentiment_analyzer import SentimentAnalyzer
        
        # Mock the pipeline
        mock_pipeline.return_value = Mock()
        
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text(None)
        
        assert result['sentiment'] == 'neutral'
        assert result['confidence'] == 0.0
    
    @patch('sentiment_analyzer.pipeline')
    def test_get_sentiment_summary(self, mock_pipeline):
        """Test sentiment summary calculation"""
        from sentiment_analyzer import SentimentAnalyzer
        
        # Mock the pipeline
        mock_pipeline.return_value = Mock()
        
        # Create test dataframe
        df = pd.DataFrame({
            'sentiment': ['positive', 'positive', 'negative', 'neutral'],
            'confidence': [0.9, 0.8, 0.7, 0.6],
            'stars': [5, 4, 2, 3]
        })
        
        analyzer = SentimentAnalyzer()
        summary = analyzer.get_sentiment_summary(df)
        
        assert summary['total_reviews'] == 4
        assert summary['positive'] == 2
        assert summary['negative'] == 1
        assert summary['neutral'] == 1
        assert summary['positive_percent'] == 50.0
        assert abs(summary['average_confidence'] - 0.75) < 0.0001
        assert summary['average_stars'] == 3.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
