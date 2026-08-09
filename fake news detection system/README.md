# Fake News Detection System

## 📰 Project Overview

A comprehensive Machine Learning and Natural Language Processing system that automatically detects fake news articles. This mini-project uses advanced ML algorithms (Logistic Regression, Naive Bayes, SVM) combined with TF-IDF vectorization to classify news as real or fake with high accuracy.

## 📊 Dataset

This project uses the **"Fake and real news dataset"** from Kaggle:

- **Source**: [Fake and real news dataset by Clément Bisaillon](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- **Size**: 44,898 articles (23,481 Fake + 21,417 Real)
- **Content**: News articles with title, text, subject, and date
- **License**: CC0: Public Domain
- **Training Set**: 10,000 samples (5,000 fake + 5,000 real) for fast training
- **Publication Year**: 2017

### Dataset Citation
```
Bisaillon, C. (2020). Fake and real news dataset. Kaggle. 
https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
```

**Note**: The dataset files (`Fake.csv` and `True.csv`) should be downloaded from Kaggle and placed in the project root directory before training.

## 🎯 Features

- **Multiple ML Models**: Implements and compares Logistic Regression, Naive Bayes, and SVM
- **Advanced NLP**: Text preprocessing with tokenization, stop word removal, and lemmatization
- **TF-IDF Vectorization**: Converts text into numerical features using n-grams
- **Web Interface**: User-friendly Flask web application
- **Real-time Predictions**: Instant news verification with confidence scores
- **Model Comparison**: Automatic evaluation and selection of best-performing model
- **Responsive Design**: Modern, mobile-friendly UI

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask
- **ML Libraries**: Scikit-learn
- **NLP**: NLTK (Natural Language Toolkit)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Model Persistence**: Pickle

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd fake-news-detection-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download NLTK Data

The system will automatically download required NLTK data on first run, but you can pre-download it:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## 📊 Usage

### Step 1: Train the Models

First, train the machine learning models using the sample dataset:

```bash
python train.py
```

This will:
- Load/create the training dataset
- Preprocess the text data
- Extract TF-IDF features
- Train three different models (Logistic Regression, Naive Bayes, SVM)
- Compare model performance
- Save the best model and vectorizer

**Output**: Trained models will be saved in the `models/` directory.

### Step 2: Run the Web Application

Start the Flask server:

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

### Step 3: Verify News

1. Open your browser and go to `http://localhost:5000`
2. Enter or paste a news article in the text area
3. Click "Analyze News"
4. View the prediction result with confidence score

## 📁 Project Structure

```
fake-news-detection-system/
│
├── app.py                      # Flask web application
├── train.py                    # Model training script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/                       # Dataset directory
│   └── (your datasets here)
│
├── models/                     # Trained models (generated)
│   ├── best_model.pkl
│   ├── logistic_regression.pkl
│   ├── naive_bayes.pkl
│   ├── svm.pkl
│   └── tfidf_vectorizer.pkl
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── preprocessing.py        # Text preprocessing
│   ├── feature_extraction.py  # TF-IDF vectorization
│   ├── data_loader.py          # Dataset management
│   └── helpers.py              # Helper functions
│
├── models/                     # ML models
│   └── classifier.py           # Model implementations
│
├── templates/                  # HTML templates
│   ├── index.html              # Home page
│   ├── about.html              # About page
│   ├── 404.html                # Error page
│   └── 500.html                # Error page
│
└── static/                     # Static files
    ├── css/
    │   └── style.css           # Stylesheets
    └── js/
        └── main.js             # JavaScript
```

## 🔬 How It Works

### 1. Data Preprocessing
- Remove URLs, HTML tags, mentions, and hashtags
- Convert text to lowercase
- Remove punctuation and numbers
- Tokenize text
- Remove stop words
- Apply lemmatization

### 2. Feature Extraction
- Convert text to numerical features using TF-IDF
- Use unigrams and bigrams (n-gram range: 1-2)
- Limit to top 5000 features
- Apply min/max document frequency filtering

### 3. Model Training
Three models are trained and compared:
- **Logistic Regression**: Linear model with L2 regularization
- **Naive Bayes**: Multinomial probabilistic classifier
- **Support Vector Machine**: Linear kernel SVM

### 4. Model Evaluation
Models are evaluated using:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

### 5. Prediction
- Best performing model is selected automatically
- Provides binary classification (Real/Fake)
- Returns confidence score (probability)

## 📈 Model Performance

**Current Model**: Multinomial Naive Bayes trained on Kaggle dataset (10,000 samples)

**Training Results**:
- **Accuracy**: 91.95%
- **Training Samples**: 8,000
- **Test Samples**: 2,000
- **TF-IDF Features**: 2,000
- **Training Time**: ~2 minutes

**Performance Breakdown**:

| Metric | Real News | Fake News |
|--------|-----------|-----------|
| Precision | 0.92 | 0.92 |
| Recall | 0.92 | 0.92 |
| F1-Score | 0.92 | 0.92 |

**Confusion Matrix**:
- True Real (Correct): 920
- False Fake (Misclassified): 80
- False Real (Misclassified): 81
- True Fake (Correct): 919

*Note: This is a fast-training model optimized for speed. Accuracy can be improved by training on the full dataset (44,898 articles) with SVM or Logistic Regression, though training time increases to 10-30 minutes.*

## 🗃️ Using Custom Datasets

To train with your own dataset:

1. Prepare a CSV file with two columns:
   - `text`: News article text
   - `label`: 0 for real news, 1 for fake news

2. Place the CSV file in the `data/` directory

3. Modify `train.py`:
```python
train_models(use_sample_data=False, data_path='data/your_dataset.csv')
```

## 🔧 Configuration

### Model Parameters

Edit `models/classifier.py` to adjust model parameters:

```python
# Logistic Regression
LogisticRegression(max_iter=1000, C=1.0, random_state=42)

# Naive Bayes
MultinomialNB(alpha=1.0)

# SVM
SVC(kernel='linear', C=1.0, probability=True, random_state=42)
```

### Feature Extraction

Edit `utils/feature_extraction.py` to adjust TF-IDF parameters:

```python
TfidfVectorizer(
    max_features=5000,      # Maximum number of features
    ngram_range=(1, 2),     # Unigrams and bigrams
    min_df=2,               # Minimum document frequency
    max_df=0.8              # Maximum document frequency
)
```

## 🌐 API Endpoints

### Prediction API
```
POST /predict
Content-Type: application/json

{
    "text": "Your news article text here"
}

Response:
{
    "label": "FAKE" or "REAL",
    "confidence": 85.5,
    "message": "This article appears to be fake news.",
    "color": "red" or "green"
}
```

### Health Check
```
GET /api/health

Response:
{
    "status": "running",
    "model_loaded": true,
    "vectorizer_loaded": true,
    "preprocessor_loaded": true
}
```

## 🎓 Educational Purpose

This project demonstrates:
- Text preprocessing and NLP techniques
- Feature engineering with TF-IDF
- Supervised learning classification
- Model comparison and evaluation
- Building ML-powered web applications
- Flask REST API development
- Responsive web design

## ⚠️ Disclaimer

This system is designed for educational purposes and should not be the sole source for verifying news authenticity. Always:
- Cross-reference with multiple reliable sources
- Check the original source credibility
- Use critical thinking
- Verify facts with reputable fact-checking organizations

## 🚀 Future Enhancements

- [ ] Integration with real-time news APIs
- [ ] Deep learning models (LSTM, BERT, Transformers)
- [ ] Multi-language support
- [ ] Source credibility scoring
- [ ] Fact-checking database integration
- [ ] Chrome/Firefox browser extension
- [ ] User feedback mechanism
- [ ] Historical prediction tracking
- [ ] Batch processing for multiple articles
- [ ] RESTful API with authentication

## 📝 License

This project is open-source and available for educational purposes.

## 👨‍💻 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Contact

For questions or feedback about this project, please open an issue in the repository.

## 🙏 Acknowledgments

- NLPT for natural language processing tools
- Scikit-learn for machine learning algorithms
- Flask for web framework
- The open-source community

---

**Built with ❤️ using Python, Machine Learning, and NLP**

*Last Updated: October 2025*
