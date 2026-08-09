"""
Full Dataset Training - Optimized for Speed
Trains on all 44,898 Kaggle articles with speed optimizations
Target: Complete in ~10 minutes
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from utils.preprocessing import TextPreprocessor
import time
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("FULL DATASET TRAINING - SPEED OPTIMIZED")
print("Training on 44,898 articles from Kaggle")
print("=" * 70)
print()

start_time = time.time()

# Initialize preprocessor
print("✓ Initializing preprocessor...")
preprocessor = TextPreprocessor()

# Load full datasets
print("\n[1/6] Loading Kaggle dataset files...")
load_start = time.time()
fake_df = pd.read_csv('Fake.csv')
true_df = pd.read_csv('True.csv')
print(f"  ✓ Fake articles: {len(fake_df):,}")
print(f"  ✓ Real articles: {len(true_df):,}")

# Add labels
fake_df['label'] = 1
true_df['label'] = 0

# Combine all data
df = pd.concat([fake_df, true_df], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print(f"  ✓ Total articles: {len(df):,}")
print(f"  ⏱ Loading time: {time.time() - load_start:.1f}s")

# Combine title and text
print("\n[2/6] Combining title and text...")
combine_start = time.time()
df['content'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
print(f"  ⏱ Time: {time.time() - combine_start:.1f}s")

# Preprocess (this is the slowest part)
print("\n[3/6] Preprocessing text (this takes longest - ~3-5 minutes)...")
print("  Processing in batches with progress updates...")
preprocess_start = time.time()

processed_texts = []
batch_size = 5000
total_batches = (len(df) + batch_size - 1) // batch_size

for i in range(0, len(df), batch_size):
    batch = df['content'].iloc[i:i+batch_size]
    batch_processed = batch.apply(preprocessor.preprocess)
    processed_texts.extend(batch_processed.tolist())
    
    current_batch = (i // batch_size) + 1
    percent = (current_batch / total_batches) * 100
    print(f"    Batch {current_batch}/{total_batches} ({percent:.1f}%) - "
          f"Processed {min(i+batch_size, len(df)):,}/{len(df):,} articles", end='\r')

df['processed_text'] = processed_texts
print(f"\n  ✓ Preprocessing completed!")
print(f"  ⏱ Time: {time.time() - preprocess_start:.1f}s")

# Split data
print("\n[4/6] Splitting data (80% train, 20% test)...")
split_start = time.time()
X_train, X_test, y_train, y_test = train_test_split(
    df['processed_text'], 
    df['label'], 
    test_size=0.2, 
    random_state=42,
    stratify=df['label']
)
print(f"  ✓ Training samples: {len(X_train):,}")
print(f"  ✓ Testing samples: {len(X_test):,}")
print(f"  ⏱ Time: {time.time() - split_start:.1f}s")

# TF-IDF Vectorization
print("\n[5/6] Creating TF-IDF features...")
tfidf_start = time.time()
vectorizer = TfidfVectorizer(
    max_features=3000,        # Balanced: speed vs accuracy
    ngram_range=(1, 2),       # Unigrams + bigrams
    min_df=3,                 # Minimum document frequency
    max_df=0.8,              # Maximum document frequency
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"  ✓ Features extracted: {X_train_tfidf.shape[1]:,}")
print(f"  ⏱ Time: {time.time() - tfidf_start:.1f}s")

# Train Logistic Regression (fast and accurate)
print("\n[6/6] Training Logistic Regression model...")
train_start = time.time()
model = LogisticRegression(
    max_iter=100,            # Reduced iterations for speed
    C=1.0,
    solver='saga',           # Fastest solver for large datasets
    random_state=42,
    n_jobs=-1                # Use all CPU cores
)
model.fit(X_train_tfidf, y_train)
print(f"  ✓ Training completed!")
print(f"  ⏱ Time: {time.time() - train_start:.1f}s")

# Evaluate
print("\n" + "=" * 70)
print("EVALUATING MODEL")
print("=" * 70)
eval_start = time.time()
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"⏱ Evaluation time: {time.time() - eval_start:.1f}s")

print("\n" + "=" * 70)
print("RESULTS - FULL DATASET TRAINING")
print("=" * 70)
print(f"\n🎯 Accuracy: {accuracy * 100:.2f}%")
print(f"📊 Training Samples: {len(X_train):,}")
print(f"📊 Test Samples: {len(X_test):,}")
print(f"🔧 TF-IDF Features: {X_train_tfidf.shape[1]:,}")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))

print("📊 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"  ✓ True Real: {cm[0][0]:,}")
print(f"  ✗ False Fake: {cm[0][1]:,}")
print(f"  ✗ False Real: {cm[1][0]:,}")
print(f"  ✓ True Fake: {cm[1][1]:,}")

# Save models
print("\n" + "=" * 70)
print("SAVING MODELS")
print("=" * 70)

print("💾 Saving TF-IDF vectorizer...")
with open('models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print("  ✓ Saved: models/tfidf_vectorizer.pkl")

print("💾 Saving Logistic Regression model...")
with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("  ✓ Saved: models/best_model.pkl")

with open('models/logistic_regression.pkl', 'wb') as f:
    pickle.dump(model, f)
print("  ✓ Saved: models/logistic_regression.pkl")

# Total time
total_time = time.time() - start_time
minutes = int(total_time // 60)
seconds = int(total_time % 60)

print("\n" + "=" * 70)
print("TRAINING SUMMARY")
print("=" * 70)
print(f"⏱ Total Time: {minutes}m {seconds}s")
print(f"🎯 Final Accuracy: {accuracy * 100:.2f}%")
print(f"📊 Dataset Size: {len(df):,} articles")
print(f"🤖 Model: Logistic Regression")
print(f"🔧 Features: {X_train_tfidf.shape[1]:,}")
print(f"📈 Training Samples: {len(X_train):,}")
print(f"📉 Test Samples: {len(X_test):,}")

# Quick test
print("\n" + "=" * 70)
print("QUICK TEST")
print("=" * 70)

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

print("\n" + "=" * 70)
print("✅ FULL DATASET TRAINING COMPLETE!")
print("=" * 70)
print(f"🚀 Ready for deployment with {len(df):,} articles trained!")
print("=" * 70)
