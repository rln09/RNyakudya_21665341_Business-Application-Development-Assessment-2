# test_harness/unit_tests/test_models.py
import unittest
import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from unittest.mock import Mock, patch
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestStudentModel(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_db = Mock()
        self.student_model = StudentModel(self.mock_db)
        self.test_student_data = {
            'student_no': 'S001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@university.edu',
            'course_id': 1
        }
    
    def test_add_student_success(self):
        """Test successful student addition"""
        # Execute
        self.student_model.add_student(**self.test_student_data)
        
        # Verify database call
        self.mock_db.execute.assert_called_once()
        call_args = self.mock_db.execute.call_args[0]
        self.assertEqual(call_args[1], (
            'S001', 'John', 'Doe', 'john.doe@university.edu', 1
        ))
    
    def test_add_student_duplicate_email(self):
        """Test duplicate email constraint"""
        self.mock_db.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: students.email")
        
        with self.assertRaises(sqlite3.IntegrityError):
            self.student_model.add_student(**self.test_student_data)
    
    def test_delete_student_logging(self):
        """Test that student deletion is properly logged"""
        # Mock database response for student lookup
        self.mock_db.fetchone.return_value = {
            'student_no': 'S001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@university.edu',
            'course_id': 1
        }
        
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.student_model.delete_student(1)
            
            # Verify log file was written to
            mock_file.assert_called_with('logs/student_audit.log', 'a', encoding='utf-8')

class TestCourseModel(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = Mock()
        self.course_model = CourseModel(self.mock_db)
    
    def test_course_deletion_validation(self):
        """Test course deletion prevents orphaned student records"""
        # Mock student count
        self.mock_db.fetchone.return_value = (5,)  # 5 enrolled students
        
        # This should be implemented in the actual code
        with self.assertRaises(ValueError):
            self.course_model.delete_course(1)

if __name__ == '__main__':
    unittest.main()