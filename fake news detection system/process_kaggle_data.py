"""
Process Kaggle Fake News Dataset
Merges Fake.csv and True.csv into a single dataset for training
Dataset Source: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
"""

import pandas as pd
import os

def process_kaggle_dataset():
    """
    Loads and merges Fake.csv and True.csv from Kaggle dataset
    Creates a unified dataset with text and label columns
    """
    print("=" * 60)
    print("PROCESSING KAGGLE FAKE NEWS DATASET")
    print("=" * 60)
    
    # File paths
    fake_csv = "Fake.csv"
    true_csv = "True.csv"
    output_csv = "data/kaggle_news_dataset.csv"
    
    # Check if files exist
    if not os.path.exists(fake_csv):
        print(f"❌ Error: {fake_csv} not found!")
        print("Please download the dataset from Kaggle and place in project root")
        return False
    
    if not os.path.exists(true_csv):
        print(f"❌ Error: {true_csv} not found!")
        print("Please download the dataset from Kaggle and place in project root")
        return False
    
    # Load fake news
    print(f"\n📰 Loading {fake_csv}...")
    fake_df = pd.read_csv(fake_csv)
    print(f"   ✓ Loaded {len(fake_df)} fake news articles")
    
    # Load real news
    print(f"\n📰 Loading {true_csv}...")
    true_df = pd.read_csv(true_csv)
    print(f"   ✓ Loaded {len(true_df)} real news articles")
    
    # Add labels
    fake_df['label'] = 1  # 1 for fake
    true_df['label'] = 0  # 0 for real
    
    # Combine title and text for better feature extraction
    print("\n🔧 Processing text data...")
    fake_df['text'] = fake_df['title'] + ". " + fake_df['text']
    true_df['text'] = true_df['title'] + ". " + true_df['text']
    
    # Select only needed columns
    fake_df = fake_df[['text', 'label']]
    true_df = true_df[['text', 'label']]
    
    # Merge datasets
    print("\n🔄 Merging datasets...")
    combined_df = pd.concat([fake_df, true_df], ignore_index=True)
    
    # Shuffle the dataset
    print("🔀 Shuffling data...")
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Remove any null values
    print("🧹 Cleaning data...")
    initial_count = len(combined_df)
    combined_df = combined_df.dropna()
    final_count = len(combined_df)
    
    if initial_count > final_count:
        print(f"   ✓ Removed {initial_count - final_count} rows with missing data")
    
    # Save to CSV
    print(f"\n💾 Saving to {output_csv}...")
    os.makedirs('data', exist_ok=True)
    combined_df.to_csv(output_csv, index=False)
    
    # Display statistics
    print("\n" + "=" * 60)
    print("DATASET STATISTICS")
    print("=" * 60)
    print(f"Total articles: {len(combined_df)}")
    print(f"Fake news: {len(combined_df[combined_df['label'] == 1])} ({len(combined_df[combined_df['label'] == 1])/len(combined_df)*100:.2f}%)")
    print(f"Real news: {len(combined_df[combined_df['label'] == 0])} ({len(combined_df[combined_df['label'] == 0])/len(combined_df)*100:.2f}%)")
    print(f"\nAverage article length: {combined_df['text'].str.len().mean():.0f} characters")
    print(f"Minimum article length: {combined_df['text'].str.len().min()} characters")
    print(f"Maximum article length: {combined_df['text'].str.len().max()} characters")
    
    print("\n" + "=" * 60)
    print("✅ DATASET PROCESSED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📂 Output file: {output_csv}")
    print("\nNext steps:")
    print("1. Run: py -3.12 train_enhanced.py")
    print("2. This will train models with the Kaggle dataset")
    print("3. Check accuracy improvements!")
    
    return True

if __name__ == "__main__":
    process_kaggle_dataset()
