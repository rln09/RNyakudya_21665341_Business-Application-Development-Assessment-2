# test_harness/run_tests.py
#!/usr/bin/env python3
"""
Comprehensive Test Runner for Student Management System
Supports multiple test types and generates detailed reports
"""

import unittest
import argparse
import sys
import os
import json
import datetime
from pathlib import Path

class TestRunner:
    def __init__(self):
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        self.test_start_time = None
        
    def setup_logging(self):
        """Set up test logging configuration"""
        log_file = self.results_dir / f"test_run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def run_unit_tests(self, verbose=False):
        """Execute unit test suite"""
        logger = self.setup_logging()
        logger.info("Starting unit test suite...")
        
        loader = unittest.TestLoader()
        start_dir = 'test_harness/unit_tests'
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(suite)
        
        logger.info(f"Unit tests completed: {result.testsRun} tests run")
        return result.wasSuccessful()
    
    def run_integration_tests(self, verbose=False):
        """Execute integration test suite"""
        logger = self.setup_logging()
        logger.info("Starting integration test suite...")
        
        loader = unittest.TestLoader()
        start_dir = 'test_harness/integration_tests'
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(suite)
        
        logger.info(f"Integration tests completed: {result.testsRun} tests run")
        return result.wasSuccessful()
    
    def generate_test_report(self, results):
        """Generate comprehensive test report"""
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "test_suite": "Student Management System",
            "results": results,
            "summary": {
                "total_tests": sum(r["tests_run"] for r in results.values()),
                "passed": sum(1 for r in results.values() if r["success"]),
                "failed": sum(1 for r in results.values() if not r["success"])
            }
        }
        
        report_file = self.results_dir / "test_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate HTML report
        self.generate_html_report(report)
        
        return report
    
    def generate_html_report(self, report):
        """Generate human-readable HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report - Student Management System</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
                .success {{ color: green; }}
                .failure {{ color: red; }}
                .test-suite {{ margin: 10px 0; padding: 10px; border-left: 4px solid #007acc; }}
            </style>
        </head>
        <body>
            <h1>Test Execution Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Tests: {report['summary']['total_tests']}</p>
                <p>Passed: <span class="success">{report['summary']['passed']}</span></p>
                <p>Failed: <span class="failure">{report['summary']['failed']}</span></p>
            </div>
            <h2>Detailed Results</h2>
        """
        
        for suite_name, result in report['results'].items():
            status_class = "success" if result['success'] else "failure"
            html_content += f"""
            <div class="test-suite">
                <h3>{suite_name}</h3>
                <p>Status: <span class="{status_class}">{'PASSED' if result['success'] else 'FAILED'}</span></p>
                <p>Tests Run: {result['tests_run']}</p>
            </div>
            """
        
        html_content += """
            <footer>
                <p>Generated on: {}</p>
            </footer>
        </body>
        </html>
        """.format(report['timestamp'])
        
        html_file = self.results_dir / "test_report.html"
        with open(html_file, 'w') as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Run test suites for Student Management System')
    parser.add_argument('--unit', action='store_true', help='Run unit tests')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--all', action='store_true', help='Run all test suites')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    results = {}
    
    if args.unit or args.all:
        results['unit_tests'] = {
            'success': runner.run_unit_tests(args.verbose),
            'tests_run': 'N/A'  # Would be captured from test results
        }
    
    if args.integration or args.all:
        results['integration_tests'] = {
            'success': runner.run_integration_tests(args.verbose),
            'tests_run': 'N/A'  # Would be captured from test results
        }
    
    if results:
        report = runner.generate_test_report(results)
        print(f"Test report generated: {runner.results_dir / 'test_report.html'}")
        
        # Exit with error code if any tests failed
        sys.exit(0 if report['summary']['failed'] == 0 else 1)
    else:
        print("No test suites specified. Use --help for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main()