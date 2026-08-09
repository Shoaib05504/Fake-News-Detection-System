# Tests for Fake News Detection System

This directory contains unit and integration tests for the Fake News Detection System.

## Test Files

### `test_api.py`
Comprehensive test suite covering:
- **API Endpoints**: Tests for `/predict`, `/api/statistics`, `/api/history`, etc.
- **Database Operations**: Direct database function tests
- **Export Functionality**: CSV and PDF export tests
- **Input Validation**: Edge cases and error handling

## Running Tests

### Run all tests:
```powershell
cd "c:\Users\Yashas\Downloads\fake news detection system"
py -3.12 -m pytest tests/ -v
```

### Run specific test file:
```powershell
py -3.12 -m pytest tests/test_api.py -v
```

### Run with unittest (no pytest required):
```powershell
py -3.12 tests\test_api.py
```

### Run with coverage:
```powershell
py -3.12 -m pytest tests/ --cov=. --cov-report=html
```

## Test Coverage

The test suite includes:
- ✅ 20+ test cases
- ✅ API endpoint testing
- ✅ Database CRUD operations
- ✅ Input validation
- ✅ Statistics calculation
- ✅ Export functionality (CSV, PDF)
- ✅ Error handling
- ✅ Edge cases

## Test Database

Tests use a separate SQLite database (`test_predictions.db` and `test_db_operations.db`) that is automatically created and cleaned up after tests run.

## Adding New Tests

1. Add test methods to existing classes or create new test classes
2. Follow naming convention: `test_<description>`
3. Use `setUp()` and `tearDown()` for test isolation
4. Use descriptive assertion messages

## Example Test Output

```
test_clear_history_endpoint ... ok
test_export_csv_endpoint ... ok
test_export_pdf_endpoint ... ok
test_get_nonexistent_prediction ... ok
test_get_single_prediction ... ok
test_history_endpoint ... ok
test_home_page_loads ... ok
test_predict_endpoint_fake_news ... ok
test_predict_endpoint_real_news ... ok
test_statistics_endpoint ... ok

----------------------------------------------------------------------
Ran 20 tests in 2.145s

OK
```
