"""
Enhanced Training Script with Larger Dataset
Trains models with the comprehensive news dataset
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import DataLoader
from utils.preprocessing import TextPreprocessor
from utils.feature_extraction import FeatureExtractor
from models.classifier import FakeNewsClassifier, ModelComparison


def train_with_dataset():
    """Train models with the comprehensive dataset"""
    print("="*70)
    print("FAKE NEWS DETECTION - ENHANCED MODEL TRAINING")
    print("="*70)
    
    # Step 1: Load Data
    print("\n[1/6] Loading Kaggle fake news dataset...")
    data_loader = DataLoader()
    
    # Load the Kaggle dataset (priority: kaggle_news_dataset.csv > news_dataset.csv)
    kaggle_path = 'data/kaggle_news_dataset.csv'
    fallback_path = 'data/news_dataset.csv'
    
    if os.path.exists(kaggle_path):
        print(f"✓ Loading Kaggle dataset from {kaggle_path}")
        print("   Dataset Source: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        data_loader.load_csv(kaggle_path)
    elif os.path.exists(fallback_path):
        print(f"✓ Loading dataset from {fallback_path}")
        data_loader.load_csv(fallback_path)
    else:
        print(f"Warning: Dataset not found!")
        print("Please run: py -3.12 process_kaggle_data.py")
        print("Creating sample dataset instead...")
        data_loader.create_sample_dataset()
    
    # Display data info
    info = data_loader.get_data_info()
    print(f"\nDataset Information:")
    print(f"  Total samples: {info['total_samples']}")
    print(f"  Real news: {info['real_news']}")
    print(f"  Fake news: {info['fake_news']}")
    print(f"  Balance ratio: {info['real_news']/info['total_samples']*100:.1f}% real, {info['fake_news']/info['total_samples']*100:.1f}% fake")
    
    # Step 2: Split Data
    print("\n[2/6] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = data_loader.split_data(test_size=0.25)
    
    # Step 3: Preprocess Text
    print("\n[3/6] Preprocessing text with NLP techniques...")
    print("  - Removing URLs, HTML tags, special characters")
    print("  - Tokenization and lowercasing")
    print("  - Stop word removal")
    print("  - Lemmatization")
    
    preprocessor = TextPreprocessor(use_lemmatization=True)
    
    X_train_processed = preprocessor.preprocess_batch(X_train.tolist())
    X_test_processed = preprocessor.preprocess_batch(X_test.tolist())
    
    print(f"\nSample original text:")
    print(f"  '{X_train.iloc[0][:80]}...'")
    print(f"Sample preprocessed text:")
    print(f"  '{X_train_processed[0][:80]}...'")
    
    # Step 4: Extract Features
    print("\n[4/6] Extracting features using TF-IDF vectorization...")
    feature_extractor = FeatureExtractor(method='tfidf', max_features=5000, ngram_range=(1, 2))
    
    X_train_features = feature_extractor.fit_transform(X_train_processed)
    X_test_features = feature_extractor.transform(X_test_processed)
    
    print(f"  Feature matrix shape: {X_train_features.shape}")
    print(f"  Number of features: {X_train_features.shape[1]}")
    print(f"  Number of training samples: {X_train_features.shape[0]}")
    
    # Save vectorizer
    os.makedirs('models', exist_ok=True)
    feature_extractor.save_vectorizer('models/tfidf_vectorizer.pkl')
    
    # Step 5: Train Models
    print("\n[5/6] Training multiple machine learning models...")
    
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
    print("\n[6/6] Evaluating model performance...")
    comparison.evaluate_all(X_test_features, y_test)
    
    # Print comparison
    comparison.print_comparison()
    
    # Save all models
    print("\n" + "="*70)
    print("Saving trained models...")
    print("="*70)
    
    for name, model in comparison.models.items():
        filename = name.lower().replace(' ', '_') + '.pkl'
        model.save_model(f'models/{filename}')
    
    # Get and save best model
    best_name, best_score = comparison.get_best_model()
    best_model = comparison.models[best_name]
    best_model.save_model('models/best_model.pkl')
    
    print("\n" + "="*70)
    print("✓ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📊 Best Model: {best_name}")
    print(f"📈 Accuracy: {best_score:.4f} ({best_score*100:.2f}%)")
    print(f"\n💾 All models saved in 'models/' directory:")
    print(f"   - logistic_regression.pkl")
    print(f"   - naive_bayes.pkl")
    print(f"   - svm.pkl")
    print(f"   - best_model.pkl")
    print(f"   - tfidf_vectorizer.pkl")
    print(f"\n🚀 Ready to use! Run 'python app.py' to start the web application")


if __name__ == "__main__":
    train_with_dataset()
