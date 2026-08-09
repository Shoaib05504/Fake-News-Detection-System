"""
Configuration file for Fake News Detection System
"""

import os

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    
    # Model settings
    MODEL_DIR = 'models'
    BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.pkl')
    VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    
    # Data settings
    DATA_DIR = 'data'
    
    # NLP settings
    USE_STEMMING = False
    USE_LEMMATIZATION = True
    MIN_TEXT_LENGTH = 10
    
    # Feature extraction settings
    TFIDF_MAX_FEATURES = 5000
    TFIDF_NGRAM_RANGE = (1, 2)
    TFIDF_MIN_DF = 2
    TFIDF_MAX_DF = 0.8


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
