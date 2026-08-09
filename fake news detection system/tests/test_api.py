"""
Unit tests for Fake News Detection API endpoints
Tests prediction, statistics, history, and export functionality
"""

import unittest
import json
import sys
import os
from io import BytesIO

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import database


class TestFakeNewsAPI(unittest.TestCase):
    """Test cases for the Fake News Detection API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by all tests"""
        # Use a test database
        database.DATABASE_PATH = 'test_predictions.db'
        database.init_database()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Remove test database
        if os.path.exists('test_predictions.db'):
            os.remove('test_predictions.db')
    
    def setUp(self):
        """Set up before each test"""
        # Clear database before each test
        database.delete_all_predictions()
    
    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fake News Detector', response.data)
    
    def test_about_page_loads(self):
        """Test that the about page loads successfully"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)
    
    def test_predict_endpoint_fake_news(self):
        """Test prediction endpoint with fake news sample"""
        fake_text = "BREAKING NEWS Aliens have landed in New York City and are selling hot dogs government confirms this shocking revelation"
        
        response = self.client.post('/predict',
                                    data=json.dumps({'text': fake_text}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('label', data)
        self.assertIn('confidence', data)
        self.assertIn('message', data)
        self.assertIn(data['label'], ['FAKE', 'REAL'])
        self.assertGreater(data['confidence'], 0)
        self.assertLessEqual(data['confidence'], 100)
    
    def test_predict_endpoint_real_news(self):
        """Test prediction endpoint with real news sample"""
        real_text = "Washington (Reuters) - The United States Department of Agriculture announced new regulations for organic farming practices today."
        
        response = self.client.post('/predict',
                                    data=json.dumps({'text': real_text}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('label', data)
        self.assertIn('confidence', data)
        self.assertIn('message', data)
    
    def test_predict_endpoint_validation_short_text(self):
        """Test that short text is rejected"""
        response = self.client.post('/predict',
                                    data=json.dumps({'text': 'Hi'}),
                                    content_type='application/json')
        
        # Should return error for too short text
        self.assertEqual(response.status_code, 400)
    
    def test_predict_endpoint_missing_text(self):
        """Test that missing text field returns error"""
        response = self.client.post('/predict',
                                    data=json.dumps({}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_statistics_endpoint(self):
        """Test statistics endpoint"""
        # Add some test predictions
        database.save_prediction("Test text 1", "FAKE", 95.5, "This is likely fake", "127.0.0.1")
        database.save_prediction("Test text 2", "REAL", 87.3, "This appears real", "127.0.0.1")
        database.save_prediction("Test text 3", "FAKE", 92.1, "This is likely fake", "127.0.0.1")
        
        response = self.client.get('/api/statistics')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['total_predictions'], 3)
        self.assertEqual(data['fake_count'], 2)
        self.assertEqual(data['real_count'], 1)
        self.assertGreater(data['average_confidence'], 0)
    
    def test_history_endpoint(self):
        """Test history endpoint"""
        # Add test predictions
        database.save_prediction("Test text 1", "FAKE", 95.5, "This is likely fake", "127.0.0.1")
        database.save_prediction("Test text 2", "REAL", 87.3, "This appears real", "127.0.0.1")
        
        response = self.client.get('/api/history?limit=10')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['history']), 2)
        
        # Verify history structure
        first_item = data['history'][0]
        self.assertIn('id', first_item)
        self.assertIn('text_preview', first_item)
        self.assertIn('prediction', first_item)
        self.assertIn('confidence', first_item)
        self.assertIn('timestamp', first_item)
    
    def test_get_single_prediction(self):
        """Test retrieving a single prediction by ID"""
        # Add a test prediction
        pred_id = database.save_prediction("Full test article text", "FAKE", 95.5, "This is likely fake", "127.0.0.1")
        
        response = self.client.get(f'/api/prediction/{pred_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], pred_id)
        self.assertEqual(data['text'], "Full test article text")
        self.assertEqual(data['prediction'], "FAKE")
        self.assertEqual(data['confidence'], 95.5)
    
    def test_get_nonexistent_prediction(self):
        """Test retrieving a prediction that doesn't exist"""
        response = self.client.get('/api/prediction/99999')
        self.assertEqual(response.status_code, 404)
    
    def test_clear_history_endpoint(self):
        """Test clearing all history"""
        # Add some test predictions
        database.save_prediction("Test 1", "FAKE", 95.5, "Message", "127.0.0.1")
        database.save_prediction("Test 2", "REAL", 87.3, "Message", "127.0.0.1")
        database.save_prediction("Test 3", "FAKE", 92.1, "Message", "127.0.0.1")
        
        # Verify predictions exist
        stats_before = database.get_statistics()
        self.assertEqual(stats_before['total_predictions'], 3)
        
        # Clear history
        response = self.client.post('/api/clear-history')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_count'], 3)
        
        # Verify predictions are deleted
        stats_after = database.get_statistics()
        self.assertEqual(stats_after['total_predictions'], 0)
    
    def test_export_csv_endpoint(self):
        """Test CSV export endpoint"""
        # Add test predictions
        database.save_prediction("Test text 1", "FAKE", 95.5, "Message 1", "127.0.0.1")
        database.save_prediction("Test text 2", "REAL", 87.3, "Message 2", "127.0.0.1")
        
        response = self.client.get('/api/export-all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/csv; charset=utf-8')
        
        # Verify CSV contains data
        csv_data = response.data.decode('utf-8')
        self.assertIn('Test text 1', csv_data)
        self.assertIn('Test text 2', csv_data)
        self.assertIn('FAKE', csv_data)
        self.assertIn('REAL', csv_data)
    
    def test_export_pdf_endpoint(self):
        """Test PDF export endpoint"""
        # Add test predictions
        database.save_prediction("Test text for PDF", "FAKE", 95.5, "Message", "127.0.0.1")
        
        response = self.client.get('/api/export-all-pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')
        
        # Verify PDF data starts with PDF header
        self.assertTrue(response.data.startswith(b'%PDF'))


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations directly"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        database.DATABASE_PATH = 'test_db_operations.db'
        database.init_database()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        if os.path.exists('test_db_operations.db'):
            os.remove('test_db_operations.db')
    
    def setUp(self):
        """Clear database before each test"""
        database.delete_all_predictions()
    
    def test_save_prediction(self):
        """Test saving a prediction to database"""
        pred_id = database.save_prediction(
            text="Test article text",
            prediction="FAKE",
            confidence=95.5,
            message="This is likely fake news",
            ip_address="192.168.1.1"
        )
        
        self.assertIsNotNone(pred_id)
        self.assertGreater(pred_id, 0)
    
    def test_get_all_predictions(self):
        """Test retrieving all predictions"""
        # Add multiple predictions
        database.save_prediction("Text 1", "FAKE", 95.5, "Message 1", "127.0.0.1")
        database.save_prediction("Text 2", "REAL", 87.3, "Message 2", "127.0.0.1")
        database.save_prediction("Text 3", "FAKE", 92.1, "Message 3", "127.0.0.1")
        
        all_preds = database.get_all_predictions(limit=100)
        self.assertEqual(len(all_preds), 3)
    
    def test_get_statistics(self):
        """Test statistics calculation"""
        database.save_prediction("Text 1", "FAKE", 90.0, "Message", "127.0.0.1")
        database.save_prediction("Text 2", "FAKE", 80.0, "Message", "127.0.0.1")
        database.save_prediction("Text 3", "REAL", 70.0, "Message", "127.0.0.1")
        
        stats = database.get_statistics()
        
        self.assertEqual(stats['total_predictions'], 3)
        self.assertEqual(stats['fake_count'], 2)
        self.assertEqual(stats['real_count'], 1)
        self.assertEqual(stats['average_confidence'], 80.0)
    
    def test_delete_all_predictions(self):
        """Test deleting all predictions"""
        database.save_prediction("Text 1", "FAKE", 95.5, "Message", "127.0.0.1")
        database.save_prediction("Text 2", "REAL", 87.3, "Message", "127.0.0.1")
        
        deleted_count = database.delete_all_predictions()
        self.assertEqual(deleted_count, 2)
        
        stats = database.get_statistics()
        self.assertEqual(stats['total_predictions'], 0)
    
    def test_get_prediction_by_id(self):
        """Test retrieving prediction by specific ID"""
        pred_id = database.save_prediction(
            "Specific test text",
            "FAKE",
            95.5,
            "Test message",
            "127.0.0.1"
        )
        
        prediction = database.get_prediction_by_id(pred_id)
        
        self.assertIsNotNone(prediction)
        self.assertEqual(prediction['id'], pred_id)
        self.assertEqual(prediction['text'], "Specific test text")
        self.assertEqual(prediction['prediction'], "FAKE")
        self.assertEqual(prediction['confidence'], 95.5)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
