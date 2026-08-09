"""
Utility functions for the Fake News Detection System
"""

import os


def create_directories():
    """Create necessary directories for the project"""
    directories = [
        'data',
        'models',
        'static/css',
        'static/js',
        'templates',
        'utils'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("All directories created successfully")


def format_prediction(prediction, confidence):
    """
    Format prediction results
    
    Args:
        prediction: Model prediction (0 or 1)
        confidence: Prediction confidence score
        
    Returns:
        Dictionary with formatted results
    """
    if prediction == 1:
        label = "FAKE"
        color = "red"
        message = "This article appears to be fake news."
    else:
        label = "REAL"
        color = "green"
        message = "This article appears to be genuine news."
    
    return {
        "label": label,
        "confidence": round(confidence * 100, 2),
        "color": color,
        "message": message
    }


def validate_text_input(text, min_length=10):
    """
    Validate user text input
    
    Args:
        text: Input text
        min_length: Minimum required length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or text.strip() == "":
        return False, "Please enter some text to analyze."
    
    if len(text.strip()) < min_length:
        return False, f"Text is too short. Please enter at least {min_length} characters."
    
    return True, ""
