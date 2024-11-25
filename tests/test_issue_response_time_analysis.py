import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from issue_response_time_analysis import IssueResponseTimeAnalysis
from model import Issue, Event, State

class TestIssueResponseTimeAnalysis(unittest.TestCase):
    @patch("config.get_parameter")
    def test_constructor(self, mock_get_parameter):
        # Test that the constructor initializes the user parameter.
        
        mock_get_parameter.return_value = "test_user"
        analysis = IssueResponseTimeAnalysis()
        self.assertEqual(analysis.USER, "test_user")
        mock_get_parameter.assert_called_once_with("user")

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_valid_issues(self, mock_show, mock_get_issues):
        # Test the run method with valid issues and events.
        
        mock_get_issues.return_value = [
            MagicMock(
                created_date=datetime(2024, 1, 1),
                events=[
                    MagicMock(event_date=datetime(2024, 1, 3)),
                    MagicMock(event_date=datetime(2024, 1, 5)),
                ],
            ),
            MagicMock(
                created_date=datetime(2024, 2, 1),
                events=[
                    MagicMock(event_date=datetime(2024, 2, 2)),
                ],
            ),
        ]

        analysis = IssueResponseTimeAnalysis()
        analysis.run()
        mock_show.assert_called_once()

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_no_events(self, mock_show, mock_get_issues):
        # Test the run method when issues have no events.
        
        mock_get_issues.return_value = [
            MagicMock(
                created_date=datetime(2024, 1, 1),
                events=[],
            ),
            MagicMock(
                created_date=datetime(2024, 2, 1),
                events=[],
            ),
        ]

        analysis = IssueResponseTimeAnalysis()
        analysis.run()
        mock_show.assert_not_called()

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_empty_issues(self, mock_show, mock_get_issues):
        # Test the run method when there are no issues.

        mock_get_issues.return_value = []

        analysis = IssueResponseTimeAnalysis()
        analysis.run()
        mock_show.assert_not_called()

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_mixed_issues(self, mock_show, mock_get_issues):
        # Test the run method with a mix of issues with and without events.

        mock_get_issues.return_value = [
            MagicMock(
                created_date=datetime(2024, 1, 1),
                events=[
                    MagicMock(event_date=datetime(2024, 1, 2)),
                ],
            ),
            MagicMock(
                created_date=datetime(2024, 1, 1),
                events=[],
            ),
        ]

        analysis = IssueResponseTimeAnalysis()
        analysis.run()
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
