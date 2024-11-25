import unittest
from datetime import datetime, timedelta
from analysis.time_to_update_analysis import time_to_update


class TestTimeToUpdate(unittest.TestCase):

    def test_valid_issues(self):
        # Test with valid issues containing correctly formatted dates.
        issues = [
            {"number": 1, "created_date": "2024-01-01T12:00:00+0000", "updated_date": "2024-01-01T14:00:00+0000"},
            {"number": 2, "created_date": "2024-01-02T08:00:00+0000", "updated_date": "2024-01-02T10:30:00+0000"},
        ]

        result = time_to_update(issues)

        self.assertEqual(result[1], 7200)  
        self.assertEqual(result[2], 9000) 

    def test_missing_dates(self):
        # Test with issues that have missing 'created_date' or 'updated_date'.
        issues = [
            {"number": 1, "created_date": "2024-01-01T12:00:00+0000"},  
            {"number": 2, "updated_date": "2024-01-02T10:30:00+0000"},  
            {"number": 3},  
        ]

        result = time_to_update(issues)
        self.assertEqual(result, {}) 

    def test_invalid_date_format(self):
        # Test with issues containing incorrectly formatted dates.
        issues = [
            {"number": 1, "created_date": "InvalidDate", "updated_date": "2024-01-01T14:00:00+0000"},
            {"number": 2, "created_date": "2024-01-02T08:00:00+0000", "updated_date": "AnotherInvalidDate"},
        ]

        result = time_to_update(issues)
        self.assertEqual(result, {})

    def test_mixed_valid_and_invalid_issues(self):
        # Test with a mix of valid and invalid issues.
        issues = [
            {"number": 1, "created_date": "2024-01-01T12:00:00+0000", "updated_date": "2024-01-01T14:00:00+0000"},
            {"number": 2, "created_date": "InvalidDate", "updated_date": "2024-01-02T10:30:00+0000"},
            {"number": 3, "created_date": "2024-01-03T09:00:00+0000"},  
        ]

        result = time_to_update(issues)

        self.assertEqual(len(result), 1) 
        self.assertIn(1, result)
        self.assertEqual(result[1], 7200)  

    def test_empty_issues_list(self):
        # Test with an empty list of issues.
        issues = []

        result = time_to_update(issues)

        self.assertEqual(result, {}) 

    def test_large_time_difference(self):
        # Test with a large time difference between creation and update.
        issues = [
            {
                "number": 1,
                "created_date": "2023-01-01T12:00:00+0000",
                "updated_date": "2024-01-01T12:00:00+0000",  
            }
        ]

        result = time_to_update(issues)
        self.assertEqual(result[1], 365 * 24 * 3600) 


if __name__ == "__main__":
    unittest.main()
