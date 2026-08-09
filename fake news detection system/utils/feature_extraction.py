"""
Feature Extraction Module
Implements TF-IDF vectorization and other feature extraction techniques
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pickle
import os


class FeatureExtractor:
    """Class for extracting features from text"""
    
    def __init__(self, method='tfidf', max_features=5000, ngram_range=(1, 2)):
        """
        Initialize feature extractor
        
        Args:
            method: Feature extraction method ('tfidf' or 'count')
            max_features: Maximum number of features
            ngram_range: Range of n-grams to consider
        """
        self.method = method
        self.max_features = max_features
        self.ngram_range = ngram_range
        
        if method == 'tfidf':
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                min_df=2,
                max_df=0.8
            )
        elif method == 'count':
            self.vectorizer = CountVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                min_df=2,
                max_df=0.8
            )
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def fit_transform(self, texts):
        """
        Fit vectorizer and transform texts
        
        Args:
            texts: List of text strings
            
        Returns:
            Feature matrix
        """
        return self.vectorizer.fit_transform(texts)
    
    def transform(self, texts):
        """
        Transform texts using fitted vectorizer
        
        Args:
            texts: List of text strings
            
        Returns:
            Feature matrix
        """
        return self.vectorizer.transform(texts)
    
    def save_vectorizer(self, filepath):
        """
        Save vectorizer to file
        
        Args:
            filepath: Path to save vectorizer
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"Vectorizer saved to {filepath}")
    
    def load_vectorizer(self, filepath):
        """
        Load vectorizer from file
        
        Args:
            filepath: Path to load vectorizer from
        """
        with open(filepath, 'rb') as f:
            self.vectorizer = pickle.load(f)
        print(f"Vectorizer loaded from {filepath}")
    
    def get_feature_names(self):
        """
        Get feature names from vectorizer
        
        Returns:
            List of feature names
        """
        return self.vectorizer.get_feature_names_out()
