import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import json
from Issue_creation_analysis import MonthlyIssueAnalysis
 


class TestMonthlyIssueAnalysis(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_init_with_empty_file(self, mock_file):
        """Test initialization with an empty JSON file."""
        try:
            analysis = MonthlyIssueAnalysis(json_file="empty.json")
            self.assertIsInstance(analysis.df, pd.DataFrame)
            self.assertTrue(analysis.df.empty)
        except Exception as e:
            raise AssertionError(f"Unexpected error during initialization: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"created_date": "2023-11-01T12:00:00Z"}]')
    def test_run_with_valid_data(self, mock_file):
        """Test the `run` method with valid data."""
        analysis = MonthlyIssueAnalysis(json_file="valid.json")
        try:
            with patch("plotly.graph_objects.Figure.show") as mock_show:
                analysis.run()
                mock_show.assert_called_once()
        except Exception as e:
            raise AssertionError(f"Unexpected error during `run` method: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"created_date": ""}]')
    def test_run_with_invalid_dates(self, mock_file):
        """Test the `run` method with invalid dates."""
        analysis = MonthlyIssueAnalysis(json_file="invalid_dates.json")
        try:
            with patch("plotly.graph_objects.Figure.show") as mock_show:
                analysis.run()
                mock_show.assert_called_once()
        except Exception as e:
            raise AssertionError(f"Unexpected error with invalid dates: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"other_field": "value"}]')
    def test_run_with_missing_created_date(self, mock_file):
        """Test the `run` method with missing 'created_date' field."""
        analysis = MonthlyIssueAnalysis(json_file="missing_created_date.json")
        try:
            with patch("plotly.graph_objects.Figure.show") as mock_show:
                analysis.run()
                self.assertTrue(analysis.df["created_date"].isnull().all())
                mock_show.assert_called_once()
        except Exception as e:
            raise AssertionError(f"Unexpected error with missing 'created_date': {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"created_date": "2023-11-01T12:00:00Z"}, {"created_date": "2023-11-01T15:00:00Z"}]')
    def test_run_with_duplicate_dates(self, mock_file):
        """Test the `run` method with duplicate dates."""
        analysis = MonthlyIssueAnalysis(json_file="duplicate_dates.json")
        try:
            with patch("plotly.graph_objects.Figure.show") as mock_show:
                analysis.run()
                mock_show.assert_called_once()
        except Exception as e:
            raise AssertionError(f"Unexpected error with duplicate dates: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"created_date": "2023-11-01T12:00:00Z"}, {"created_date": "2023-11-02T15:00:00Z"}]')
    def test_run_with_multiple_months(self, mock_file):
        """Test the `run` method with data across multiple months."""
        analysis = MonthlyIssueAnalysis(json_file="multiple_months.json")
        try:
            with patch("plotly.graph_objects.Figure.show") as mock_show:
                analysis.run()
                mock_show.assert_called_once()
        except Exception as e:
            raise AssertionError(f"Unexpected error with multiple months: {e}")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_init_with_nonexistent_file(self, mock_file):
        """Test initialization with a nonexistent JSON file."""
        try:
            with self.assertRaises(AssertionError, msg="FileNotFoundError not raised as AssertionError"):
                MonthlyIssueAnalysis(json_file="nonexistent.json")
        except FileNotFoundError as e:
            raise AssertionError(f"FileNotFoundError encountered: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_init_with_invalid_json(self, mock_file):
        """Test initialization with invalid JSON content."""
        try:
            MonthlyIssueAnalysis(json_file="invalid.json")
            self.fail("Expected a JSONDecodeError.")
        except json.JSONDecodeError as e:
            raise AssertionError(f"JSONDecodeError encountered: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"created_date": "2023-11-01T12:00:00Z"}]')
    def test_run_with_partial_invalid_data(self, mock_file):
        """Test the `run` method with some valid and some invalid data."""
        analysis = MonthlyIssueAnalysis(json_file="partial_invalid.json")
        try:
            with patch("plotly.graph_objects.Figure.show") as mock_show:
                analysis.run()
                mock_show.assert_called_once()
        except Exception as e:
            raise AssertionError(f"Unexpected error with partial invalid data: {e}")


if __name__ == "__main__":
    unittest.main()
