# test_harness/ui_tests/test_student_ui.py
import unittest
import tkinter as tk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from unittest.mock import Mock, patch
from view.student_view import StudentView

class TestStudentUI(unittest.TestCase):
    
    def setUp(self):
        """Set up UI test environment"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window during tests
        self.mock_db = Mock()
        self.student_view = StudentView(self.root, self.mock_db)
    
    def tearDown(self):
        """Clean up UI tests"""
        self.root.destroy()
    
    def test_form_validation(self):
        """Test student form validation"""
        # Test empty form
        self.assertFalse(self.student_view.validate_form())
        
        # Test partial form
        self.student_view.entries['student_no'].insert(0, 'S001')
        self.assertFalse(self.student_view.validate_form())
        
        # Test complete form
        self.student_view.entries['first_name'].insert(0, 'John')
        self.student_view.entries['last_name'].insert(0, 'Doe')
        self.student_view.entries['email'].insert(0, 'john@edu.com')
        self.student_view.entries['course'].set('Computer Science')
        
        self.assertTrue(self.student_view.validate_form())
    
    def test_theme_switching(self):
        """Test theme switching functionality"""
        initial_theme = self.student_view.theme
        
        # Switch theme
        self.student_view.toggle_theme()
        
        self.assertNotEqual(initial_theme, self.student_view.theme)
    
    @patch('tkinter.messagebox')
    def test_duplicate_student_handling(self, mock_messagebox):
        """Test duplicate student error handling"""
        # Mock database to raise integrity error
        self.mock_db.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Attempt to add duplicate student
        self.student_view.save_student()
        
        # Verify error message was shown
        mock_messagebox.showerror.assert_called_once()