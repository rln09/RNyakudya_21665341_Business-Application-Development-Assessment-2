# test_harness/manual_tests/test_scenarios.md

## Student Management Test Scenarios

### Scenario 1: Add New Student
**Preconditions:**
- At least one course exists in the system
- Application is running

Test Steps:
1. Navigate to Students tab
2. Click "Clear Fields" button
3. Fill in all required fields:
   - Student No: S1001
   - First Name: Test
   - Last Name: User
   - Email: test.user@university.edu
   - Course: Select any available course
4. Click "Add" button
5. Verify success message appears
6. Verify student appears in the table

**Expected Results:**
- Student is added successfully
- Success message displayed
- New student visible in student list

### Scenario 2: Data Validation - Invalid Email
**Test Steps:**
1. Navigate to Students tab
2. Enter invalid email: "invalid-email"
3. Fill other required fields
4. Click "Add" button

Expected Results:
- Error message about invalid email format
- Student not added to database

## Course Management Test Scenarios

### Scenario 3: Delete Course with Enrolled Students
**Preconditions:**
- Course has at least one enrolled student

**Test Steps:**
1. Navigate to Courses tab
2. Select a course with enrolled students
3. Click "Delete" button
4. Confirm deletion in dialog

**Expected Results:**
- Warning message about enrolled students
- Course deletion prevented
- Data integrity maintained