"""
Training Script for Fake News Detection Models
Trains and saves Logistic Regression, Naive Bayes, and SVM models
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import DataLoader
from utils.preprocessing import TextPreprocessor
from utils.feature_extraction import FeatureExtractor
from models.classifier import FakeNewsClassifier, ModelComparison


def train_models(use_sample_data=True, data_path=None):
    """
    Train all models
    
    Args:
        use_sample_data: Whether to use sample data
        data_path: Path to custom dataset
    """
    print("="*70)
    print("FAKE NEWS DETECTION - MODEL TRAINING")
    print("="*70)
    
    # Step 1: Load Data
    print("\n[1/6] Loading data...")
    data_loader = DataLoader()
    
    if use_sample_data:
        data_loader.create_sample_dataset()
    else:
        if data_path is None:
            raise ValueError("data_path must be provided when use_sample_data=False")
        data_loader.load_csv(data_path)
    
    # Display data info
    info = data_loader.get_data_info()
    print(f"\nDataset Information:")
    print(f"  Total samples: {info['total_samples']}")
    print(f"  Real news: {info['real_news']}")
    print(f"  Fake news: {info['fake_news']}")
    
    # Step 2: Split Data
    print("\n[2/6] Splitting data...")
    X_train, X_test, y_train, y_test = data_loader.split_data(test_size=0.2)
    
    # Step 3: Preprocess Text
    print("\n[3/6] Preprocessing text...")
    preprocessor = TextPreprocessor(use_lemmatization=True)
    
    X_train_processed = preprocessor.preprocess_batch(X_train.tolist())
    X_test_processed = preprocessor.preprocess_batch(X_test.tolist())
    
    print(f"Sample preprocessed text: {X_train_processed[0][:100]}...")
    
    # Step 4: Extract Features
    print("\n[4/6] Extracting features using TF-IDF...")
    feature_extractor = FeatureExtractor(method='tfidf', max_features=5000)
    
    X_train_features = feature_extractor.fit_transform(X_train_processed)
    X_test_features = feature_extractor.transform(X_test_processed)
    
    print(f"Feature matrix shape: {X_train_features.shape}")
    
    # Save vectorizer
    os.makedirs('models', exist_ok=True)
    feature_extractor.save_vectorizer('models/tfidf_vectorizer.pkl')
    
    # Step 5: Train Models
    print("\n[5/6] Training models...")
    
    # Create model comparison
    comparison = ModelComparison()
    
    # Add models
    comparison.add_model('Logistic Regression', 
                        FakeNewsClassifier('logistic_regression'))
    comparison.add_model('Naive Bayes', 
                        FakeNewsClassifier('naive_bayes'))
    comparison.add_model('SVM', 
                        FakeNewsClassifier('svm'))
    
    # Train all models
    comparison.train_all(X_train_features, y_train)
    
    # Step 6: Evaluate Models
    print("\n[6/6] Evaluating models...")
    comparison.evaluate_all(X_test_features, y_test)
    
    # Print comparison
    comparison.print_comparison()
    
    # Save all models
    print("\nSaving models...")
    for name, model in comparison.models.items():
        filename = name.lower().replace(' ', '_') + '.pkl'
        model.save_model(f'models/{filename}')
    
    # Get and save best model
    best_name, best_score = comparison.get_best_model()
    best_model = comparison.models[best_name]
    best_model.save_model('models/best_model.pkl')
    
    print("\n" + "="*70)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\nBest Model: {best_name}")
    print(f"Accuracy: {best_score:.4f}")
    print(f"\nAll models saved in 'models/' directory")
    print(f"Vectorizer saved as 'models/tfidf_vectorizer.pkl'")


if __name__ == "__main__":
    # Train with sample data
    train_models(use_sample_data=True)
    
    # To train with your own dataset, use:
    # train_models(use_sample_data=False, data_path='data/your_dataset.csv')
