"""
Text Preprocessing Module for Fake News Detection
Handles text cleaning, tokenization, and stop word removal
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
for resource in ['tokenizers/punkt', 'corpora/stopwords', 'corpora/wordnet', 'tokenizers/punkt_tab']:
    try:
        nltk.data.find(resource)
    except LookupError:
        try:
            pkg_name = resource.split('/')[-1]
            nltk.download(pkg_name, quiet=True)
        except Exception:
            pass


class TextPreprocessor:
    """Class for preprocessing text data"""
    
    def __init__(self, use_stemming=False, use_lemmatization=True):
        """
        Initialize preprocessor
        
        Args:
            use_stemming: Whether to use stemming
            use_lemmatization: Whether to use lemmatization
        """
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.use_stemming = use_stemming
        self.use_lemmatization = use_lemmatization
    
    def clean_text(self, text):
        """
        Clean text by removing URLs, special characters, and extra spaces
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove publisher signatures and watermarks
        text = re.sub(r'^[\w\s,–-]+\(reuters\)\s*[-–]\s*', '', text)
        text = re.sub(r'\b(reuters|21st century wire|breitbart)\b', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def remove_stopwords(self, text):
        """
        Remove stop words from text
        
        Args:
            text: Input text string
            
        Returns:
            Text with stop words removed
        """
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def stem_text(self, text):
        """
        Apply stemming to text
        
        Args:
            text: Input text string
            
        Returns:
            Stemmed text
        """
        words = word_tokenize(text)
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)
    
    def lemmatize_text(self, text):
        """
        Apply lemmatization to text
        
        Args:
            text: Input text string
            
        Returns:
            Lemmatized text
        """
        words = word_tokenize(text)
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text: Input text string
            
        Returns:
            Preprocessed text
        """
        # Clean text
        text = self.clean_text(text)
        
        # Remove stop words
        text = self.remove_stopwords(text)
        
        # Apply stemming or lemmatization
        if self.use_stemming:
            text = self.stem_text(text)
        elif self.use_lemmatization:
            text = self.lemmatize_text(text)
        
        return text
    
    def preprocess_batch(self, texts):
        """
        Preprocess a batch of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of preprocessed texts
        """
        return [self.preprocess(text) for text in texts]
