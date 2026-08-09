"""
Test which samples work correctly with the new model
"""
import pickle
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from utils.preprocessing import TextPreprocessor

# Load model and vectorizer
with open('models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

preprocessor = TextPreprocessor()

# Test samples
fake_samples = [
    "BREAKING NEWS Aliens have landed in New York City and are selling hot dogs government confirms this is the biggest discovery of the century scientists shocked",
    "SHOCKING DISCOVERY Scientists confirm drinking only soda cures all diseases government hiding this secret for years pharmaceutical companies panicking"
]

real_samples = [
    "Technology companies announce partnership for artificial intelligence development and research. The collaboration aims to advance research in machine learning and natural language processing for various applications.",
    "Scientists report breakthrough in renewable energy storage technology. The new battery system shows improved efficiency and longer lifespan compared to current lithium-ion batteries used in electric vehicles.",
    "Washington (Reuters) - The United States Department of Agriculture announced new regulations for organic food labeling standards. The updated guidelines will take effect next year and aim to provide consumers with clearer information about organic certification requirements.",
    "New York (AP) - Stock markets closed higher today as investors responded positively to recent economic data. The Dow Jones Industrial Average gained 200 points while the S&P 500 index rose by 1.2 percent during afternoon trading.",
    "London (BBC) - Scientists at Oxford University published research findings in the journal Nature describing advances in cancer treatment methodology. The peer-reviewed study examined outcomes from clinical trials conducted over three years.",
]

print("Testing FAKE samples:")
for i, text in enumerate(fake_samples, 1):
    processed = preprocessor.preprocess(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    confidence = probability[prediction] * 100
    label = "FAKE" if prediction == 1 else "REAL"
    
    status = "✓" if prediction == 1 else "✗"
    print(f"{status} Sample {i}: Predicted {label} ({confidence:.1f}%)")
    if prediction != 1:
        print(f"   Text: {text[:80]}...")

print("\n" + "="*70)
print("Testing REAL samples:")
for i, text in enumerate(real_samples, 1):
    processed = preprocessor.preprocess(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    confidence = probability[prediction] * 100
    label = "FAKE" if prediction == 1 else "REAL"
    
    status = "✓" if prediction == 0 else "✗"
    print(f"{status} Sample {i}: Predicted {label} ({confidence:.1f}%)")
    if prediction != 0:
        print(f"   Text: {text[:80]}...")
