# test_harness/test_utils/config.py
"""
Test configuration settings
"""

import os
from pathlib import Path

# Test Configuration
TEST_CONFIG = {
    'database': {
        'test_db_path': 'test_data/test_database.db',
        'backup_db_path': 'test_data/backup_database.db'
    },
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'test_results/test_execution.log'
    },
    'ui': {
        'timeout': 30,  # seconds
        'screenshot_on_failure': True
    },
    'performance': {
        'max_response_time': 2.0,  # seconds
        'concurrent_users': 10
    }
}

def get_test_data_path():
    """Get path to test data directory"""
    path = Path('test_data')
    path.mkdir(exist_ok=True)
    return path

def cleanup_test_data():
    """Clean up test data after test execution"""
    test_data_path = get_test_data_path()
    for file in test_data_path.glob('*'):
        if file.is_file():
            file.unlink()