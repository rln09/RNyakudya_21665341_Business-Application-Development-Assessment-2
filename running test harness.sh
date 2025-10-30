# Install dependencies
pip install -r test_harness/requirements.txt

# Run all tests
python test_harness/run_tests.py --all --verbose

# Run specific test suites
python test_harness/run_tests.py --unit
python test_harness/run_tests.py --integration

# Run with CI configuration
python -m pytest test_harness/ --cov=./ --cov-report=xml --html=test_report.html