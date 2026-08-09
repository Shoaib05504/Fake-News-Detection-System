"""
Quick Training Script for Fast Model Creation
Samples 10,000 articles from Kaggle dataset for rapid training
Optimized for speed while maintaining reasonable accuracy
"""

import pandas as pd
import numpy as np
import pickle
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from utils.preprocessing import TextPreprocessor
import time

print("=" * 60)
print("FAST TRAINING MODE - Optimized for Speed")
print("=" * 60)
print()

# Start timer
start_time = time.time()

# Initialize preprocessor (disable lemmatization for super fast training)
print("Initializing fast preprocessor...")
preprocessor = TextPreprocessor(use_lemmatization=False)

# Load and sample data for speed
print("Loading Kaggle dataset files...")
print("Reading Fake.csv...")
fake_df = pd.read_csv('Fake.csv', on_bad_lines='skip', low_memory=False)
print(f"  Found {len(fake_df)} fake articles")

print("Reading True.csv...")
true_df = pd.read_csv('True.csv', on_bad_lines='skip', low_memory=False)
print(f"  Found {len(true_df)} real articles")

# Sample 5000 from each for balanced, fast training
print("\nSampling 5,000 articles from each category...")
fake_sample = fake_df.sample(n=5000, random_state=42)
true_sample = true_df.sample(n=5000, random_state=42)

# Add labels
fake_sample['label'] = 1
true_sample['label'] = 0

# Combine
df = pd.concat([fake_sample, true_sample], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle

print(f"Total samples: {len(df)}")
print(f"  Fake: {len(df[df['label']==1])}")
print(f"  Real: {len(df[df['label']==0])}")

# Combine title and text
print("\nCombining title and text...")
df['content'] = df['title'].fillna('') + ' ' + df['text'].fillna('')

# Preprocess
print("Preprocessing text (this may take 30-60 seconds)...")
preprocess_start = time.time()
df['processed_text'] = df['content'].apply(preprocessor.preprocess)
preprocess_time = time.time() - preprocess_start
print(f"  Preprocessing completed in {preprocess_time:.1f} seconds")

# Split data
print("\nSplitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    df['processed_text'], 
    df['label'], 
    test_size=0.2, 
    random_state=42,
    stratify=df['label']
)

print(f"  Training samples: {len(X_train)}")
print(f"  Testing samples: {len(X_test)}")

# TF-IDF Vectorization (lightweight settings for speed)
print("\nCreating TF-IDF features (lightweight mode)...")
vectorizer = TfidfVectorizer(
    max_features=2000,        # Reduced from 5000 for speed
    ngram_range=(1, 1),       # Only unigrams for speed
    min_df=5,                 # Ignore very rare words
    max_df=0.7,              # Ignore very common words
    sublinear_tf=True
)

tfidf_start = time.time()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
tfidf_time = time.time() - tfidf_start

print(f"  TF-IDF completed in {tfidf_time:.1f} seconds")
print(f"  Features extracted: {X_train_tfidf.shape[1]}")

# Train Naive Bayes (fastest classifier)
print("\nTraining Multinomial Naive Bayes...")
train_start = time.time()
model = MultinomialNB(alpha=0.1)
model.fit(X_train_tfidf, y_train)
train_time = time.time() - train_start
print(f"  Training completed in {train_time:.1f} seconds")

# Evaluate
print("\nEvaluating model...")
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)

# Display results
print("\n" + "=" * 60)
print("TRAINING RESULTS")
print("=" * 60)
print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"  True Real (correctly classified): {cm[0][0]}")
print(f"  False Fake (real classified as fake): {cm[0][1]}")
print(f"  False Real (fake classified as real): {cm[1][0]}")
print(f"  True Fake (correctly classified): {cm[1][1]}")

# Save models
print("\n" + "=" * 60)
print("SAVING MODELS")
print("=" * 60)

print("Saving TF-IDF vectorizer...")
with open('models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print("  ✓ Saved: models/tfidf_vectorizer.pkl")

print("Saving Naive Bayes model...")
with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("  ✓ Saved: models/best_model.pkl")

# Also save as naive_bayes.pkl for reference
with open('models/naive_bayes.pkl', 'wb') as f:
    pickle.dump(model, f)
print("  ✓ Saved: models/naive_bayes.pkl")

# Total time
total_time = time.time() - start_time

print("\n" + "=" * 60)
print("TRAINING SUMMARY")
print("=" * 60)
print(f"Total training time: {total_time:.1f} seconds")
print(f"  Data loading & sampling: {preprocess_time:.1f}s")
print(f"  Text preprocessing: {preprocess_time:.1f}s")
print(f"  TF-IDF vectorization: {tfidf_time:.1f}s")
print(f"  Model training: {train_time:.1f}s")
print(f"\nFinal Accuracy: {accuracy * 100:.2f}%")
print(f"Model Type: Multinomial Naive Bayes")
print(f"Training Samples: {len(X_train)}")
print(f"TF-IDF Features: {X_train_tfidf.shape[1]}")
print("\n✓ Models ready for deployment!")
print("=" * 60)

# Quick test
print("\n" + "=" * 60)
print("QUICK TEST")
print("=" * 60)

test_texts = [
    "BREAKING NEWS Aliens spotted in New York City eating pizza government confirms",
    "Scientists report breakthrough in renewable energy technology at university research center"
]

for i, text in enumerate(test_texts, 1):
    processed = preprocessor.preprocess(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    confidence = probability[prediction] * 100
    
    label = "FAKE" if prediction == 1 else "REAL"
    print(f"\nTest {i}: {text[:60]}...")
    print(f"  Prediction: {label}")
    print(f"  Confidence: {confidence:.1f}%")

print("\n" + "=" * 60)
print("✓ FAST TRAINING COMPLETE!")
print("=" * 60)
