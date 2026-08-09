"""
Machine Learning Models for Fake News Detection
Implements Logistic Regression, Naive Bayes, and SVM classifiers
"""

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import pickle
import os
import numpy as np


class FakeNewsClassifier:
    """Base class for fake news classification models"""
    
    def __init__(self, model_type='logistic_regression'):
        """
        Initialize classifier
        
        Args:
            model_type: Type of model ('logistic_regression', 'naive_bayes', or 'svm')
        """
        self.model_type = model_type
        self.model = self._create_model()
        self.is_trained = False
    
    def _create_model(self):
        """Create the specified model"""
        if self.model_type == 'logistic_regression':
            return LogisticRegression(max_iter=1000, random_state=42)
        elif self.model_type == 'naive_bayes':
            return MultinomialNB()
        elif self.model_type == 'svm':
            return SVC(kernel='linear', probability=True, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X_train, y_train):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print(f"{self.model_type} model trained successfully!")
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Features to predict
            
        Returns:
            Array of predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Get prediction probabilities
        
        Args:
            X: Features to predict
            
        Returns:
            Array of probability predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary with evaluation metrics
        """
        y_pred = self.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted')
        }
        
        print(f"\n{self.model_type.upper()} Model Evaluation:")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1 Score: {metrics['f1_score']:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return metrics
    
    def save_model(self, filepath):
        """
        Save model to file
        
        Args:
            filepath: Path to save model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'is_trained': self.is_trained
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load model from file
        
        Args:
            filepath: Path to load model from
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from {filepath}")


class ModelComparison:
    """Class for comparing multiple models"""
    
    def __init__(self):
        """Initialize model comparison"""
        self.models = {}
        self.results = {}
    
    def add_model(self, name, model):
        """
        Add a model to comparison
        
        Args:
            name: Model name
            model: FakeNewsClassifier instance
        """
        self.models[name] = model
    
    def train_all(self, X_train, y_train):
        """
        Train all models
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        for name, model in self.models.items():
            print(f"\n{'='*50}")
            print(f"Training {name}...")
            print('='*50)
            model.train(X_train, y_train)
    
    def evaluate_all(self, X_test, y_test):
        """
        Evaluate all models
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary with all model results
        """
        for name, model in self.models.items():
            print(f"\n{'='*50}")
            print(f"Evaluating {name}...")
            print('='*50)
            metrics = model.evaluate(X_test, y_test)
            self.results[name] = metrics
        
        return self.results
    
    def get_best_model(self, metric='accuracy'):
        """
        Get the best performing model
        
        Args:
            metric: Metric to compare ('accuracy', 'precision', 'recall', 'f1_score')
            
        Returns:
            Tuple of (best_model_name, best_score)
        """
        if not self.results:
            raise ValueError("No results available. Run evaluate_all() first.")
        
        best_name = max(self.results, key=lambda k: self.results[k][metric])
        best_score = self.results[best_name][metric]
        
        return best_name, best_score
    
    def print_comparison(self):
        """Print comparison of all models"""
        if not self.results:
            print("No results available. Run evaluate_all() first.")
            return
        
        print(f"\n{'='*70}")
        print("MODEL COMPARISON")
        print('='*70)
        print(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1 Score':<12}")
        print('-'*70)
        
        for name, metrics in self.results.items():
            print(f"{name:<20} {metrics['accuracy']:<12.4f} {metrics['precision']:<12.4f} "
                  f"{metrics['recall']:<12.4f} {metrics['f1_score']:<12.4f}")
        
        print('='*70)
        
        best_name, best_score = self.get_best_model()
        print(f"\nBest Model: {best_name} (Accuracy: {best_score:.4f})")
