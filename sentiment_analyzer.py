"""
Sentiment Analysis Engine
Supports multilingual sentiment analysis including Arabic
"""

import pandas as pd
import torch
from transformers import pipeline
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class SentimentAnalyzer:
    """
    Sentiment analyzer using open-source multilingual models
    with support for Arabic and other languages
    """
    
    def __init__(self, model_name: str = "nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        Initialize sentiment analyzer with a multilingual model
        
        Args:
            model_name: HuggingFace model name (default supports Arabic)
        """
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load sentiment analysis pipeline
        print(f"Loading model: {model_name}...")
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=self.device,
            truncation=True,
            max_length=512
        )
        print("Model loaded successfully!")
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment label and score
        """
        if not text or not isinstance(text, str) or text.strip() == '':
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'stars': 3
            }
        
        try:
            result = self.sentiment_pipeline(text[:512])[0]
            label = result['label']
            score = result['score']
            
            # Convert star rating to sentiment
            if 'star' in label.lower():
                stars = int(label.split()[0])
                if stars <= 2:
                    sentiment = 'negative'
                elif stars == 3:
                    sentiment = 'neutral'
                else:
                    sentiment = 'positive'
            else:
                sentiment = label.lower()
                stars = 3
            
            return {
                'sentiment': sentiment,
                'confidence': score,
                'stars': stars
            }
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'stars': 3
            }
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Analyze sentiment for all texts in a DataFrame
        
        Args:
            df: DataFrame containing text data
            text_column: Name of column containing text to analyze
            
        Returns:
            DataFrame with added sentiment columns
        """
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in DataFrame")
        
        print(f"Analyzing {len(df)} texts...")
        
        # Analyze each text
        results = []
        for idx, text in enumerate(df[text_column]):
            if (idx + 1) % 10 == 0:
                print(f"Processed {idx + 1}/{len(df)} texts...")
            
            result = self.analyze_text(str(text))
            results.append(result)
        
        # Add results to dataframe
        result_df = df.copy()
        result_df['sentiment'] = [r['sentiment'] for r in results]
        result_df['confidence'] = [r['confidence'] for r in results]
        result_df['stars'] = [r['stars'] for r in results]
        
        print("Analysis complete!")
        return result_df
    
    def get_sentiment_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics of sentiment analysis
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Dictionary with summary statistics
        """
        if 'sentiment' not in df.columns:
            raise ValueError("DataFrame must contain 'sentiment' column")
        
        total = len(df)
        sentiment_counts = df['sentiment'].value_counts().to_dict()
        
        summary = {
            'total_reviews': total,
            'positive': sentiment_counts.get('positive', 0),
            'neutral': sentiment_counts.get('neutral', 0),
            'negative': sentiment_counts.get('negative', 0),
            'positive_percent': (sentiment_counts.get('positive', 0) / total * 100) if total > 0 else 0,
            'neutral_percent': (sentiment_counts.get('neutral', 0) / total * 100) if total > 0 else 0,
            'negative_percent': (sentiment_counts.get('negative', 0) / total * 100) if total > 0 else 0,
            'average_confidence': df['confidence'].mean() if 'confidence' in df.columns else 0,
            'average_stars': df['stars'].mean() if 'stars' in df.columns else 0
        }
        
        return summary


def load_data_file(file_path: str) -> pd.DataFrame:
    """
    Load data from CSV or XLSX file
    
    Args:
        file_path: Path to file
        
    Returns:
        DataFrame with loaded data
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("File must be CSV or XLSX format")
