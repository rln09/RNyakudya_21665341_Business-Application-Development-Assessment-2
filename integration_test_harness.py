# test_harness/integration_tests/test_crud_operations.py
import unittest
import tempfile
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from db import Database
from model.student_model import StudentModel
from model.course_model import CourseModel

class TestCRUDOperations(unittest.TestCase):
    
    def setUp(self):
        """Set up temporary database for integration tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_file = os.path.join(self.temp_dir, 'test_database.db')
        
        # Override DB_FILE for testing
        import db
        original_db_file = db.DB_FILE
        db.DB_FILE = self.db_file
        
        self.db = Database()
        self.student_model = StudentModel(self.db)
        self.course_model = CourseModel(self.db)
    
    def tearDown(self):
        """Clean up after tests"""
        self.db.close()
        import db
        db.DB_FILE = 'data/database.db'  # Restore original path
    
    def test_student_lifecycle(self):
        """Test complete student CRUD lifecycle"""
        # Create course first
        self.course_model.add_course('CS101', 'Computer Science', 'Dr. Smith', 3)
        
        # Add student
        self.student_model.add_student('S001', 'Alice', 'Johnson', 'alice@edu.com', 1)
        
        # Retrieve student
        students = self.student_model.get_all_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]['student_no'], 'S001')
        
        # Update student
        self.student_model.update_student(1, 'S001', 'Alice', 'Smith', 'alice.smith@edu.com', 1)
        
        # Verify update
        students = self.student_model.get_all_students()
        self.assertEqual(students[0]['name'], 'Alice Smith')
        
        # Delete student
        self.student_model.delete_student(1)
        
        # Verify deletion
        students = self.student_model.get_all_students()
        self.assertEqual(len(students), 0)
    
    def test_search_functionality(self):
        """Test search functionality across models"""
        # Add test data
        self.course_model.add_course('MATH101', 'Mathematics', 'Dr. Brown', 4)
        self.student_model.add_student('S002', 'Bob', 'Wilson', 'bob@edu.com', 1)
        
        # Test student search
        results = self.student_model.search_students('Bob')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['student_no'], 'S002')
        
        # Test course search
        results = self.course_model.search_courses('Math')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['course_code'], 'MATH101')