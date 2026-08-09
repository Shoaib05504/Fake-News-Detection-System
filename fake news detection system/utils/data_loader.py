"""
Data Loading and Management Module
Handles dataset loading, splitting, and management
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os


class DataLoader:
    """Class for loading and managing datasets"""
    
    def __init__(self, data_path=None):
        """
        Initialize data loader
        
        Args:
            data_path: Path to dataset file
        """
        self.data_path = data_path
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_csv(self, filepath, text_column='text', label_column='label'):
        """
        Load dataset from CSV file
        
        Args:
            filepath: Path to CSV file
            text_column: Name of text column
            label_column: Name of label column
            
        Returns:
            DataFrame with loaded data
        """
        self.data = pd.read_csv(filepath)
        print(f"Loaded {len(self.data)} records from {filepath}")
        print(f"Columns: {self.data.columns.tolist()}")
        return self.data
    
    def create_sample_dataset(self):
        """
        Create a sample dataset for testing
        
        Returns:
            DataFrame with sample data
        """
        # Sample fake news examples
        fake_news = [
            "Breaking: Aliens have landed in New York City and are selling hot dogs",
            "Scientists discover eating chocolate cures all diseases instantly",
            "Government confirms time travel will be available next week",
            "Local man grows 50-foot tall tomatoes using this one weird trick",
            "President announces free money for everyone starting tomorrow",
            "Study shows watching TV makes you smarter than reading books",
            "Miracle cure for aging discovered in common household item",
            "Breaking news: Moon is actually made of cheese, NASA admits",
            "Shocking revelation: Birds are government surveillance drones",
            "New study proves Earth is actually flat and hollow inside"
        ]
        
        # Sample real news examples
        real_news = [
            "Stock markets close mixed as investors await economic data",
            "New research shows climate change affecting global weather patterns",
            "Technology companies announce partnership for artificial intelligence development",
            "Local government approves budget for infrastructure improvements",
            "Health officials recommend annual checkups for preventive care",
            "Scientists make progress in understanding genetic disorders",
            "Education department releases new guidelines for schools",
            "Study finds exercise and diet important for heart health",
            "Economists predict moderate growth in upcoming quarter",
            "Researchers develop new method for water purification"
        ]
        
        # Create DataFrame
        texts = fake_news + real_news
        labels = [1] * len(fake_news) + [0] * len(real_news)  # 1 = fake, 0 = real
        
        self.data = pd.DataFrame({
            'text': texts,
            'label': labels
        })
        
        print(f"Created sample dataset with {len(self.data)} records")
        return self.data
    
    def split_data(self, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets
        
        Args:
            test_size: Proportion of data for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_csv() or create_sample_dataset() first.")
        
        X = self.data['text']
        y = self.data['label']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Training set: {len(self.X_train)} samples")
        print(f"Testing set: {len(self.X_test)} samples")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_data_info(self):
        """
        Get information about the loaded data
        
        Returns:
            Dictionary with data statistics
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        info = {
            "total_samples": len(self.data),
            "fake_news": len(self.data[self.data['label'] == 1]),
            "real_news": len(self.data[self.data['label'] == 0]),
            "columns": self.data.columns.tolist(),
            "null_values": self.data.isnull().sum().to_dict()
        }
        
        return info
    
    def save_dataset(self, filepath):
        """
        Save current dataset to CSV
        
        Args:
            filepath: Path to save dataset
        """
        if self.data is None:
            raise ValueError("No data to save")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.data.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
