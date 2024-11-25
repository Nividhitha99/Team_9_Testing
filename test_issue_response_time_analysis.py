import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from issue_response_time_analysis import IssueResponseTimeAnalysis
from model import Issue, Event, State

class TestIssueResponseTimeAnalysis(unittest.TestCase):
    def setUp(self):
        # Mock data for Event and Issue objects
        event_data_1 = {
            'event_type': 'comment',
            'author': 'user1',
            'event_date': '2023-01-01T11:00:00Z',  # UTC time
            'label': 'bug',
            'comment': 'First response'
        }
        event_data_2 = {
            'event_type': 'comment',
            'author': 'user2',
            'event_date': '2023-01-01T12:00:00Z',  # UTC time
            'label': 'enhancement',
            'comment': 'Second response'
        }

        # Creating Event instances from mock data
        event1 = Event(event_data_1)
        event2 = Event(event_data_2)

        # Mocking Issue with created_date and events
        self.mock_issues = [
           Issue(jobj={
                'number': 123,
                'created_date': '2023-01-01T10:00:00Z',  # UTC time
                'updated_date': '2023-01-01T12:00:00Z',  # UTC time
                'state': 'open',  # Here we use the string value of the State Enum
                'events': [event_data_1, event_data_2]
            }),
            Issue(jobj={
                'number': 124,
                'created_date': '2023-01-01T09:00:00Z',  # UTC time
                'updated_date': '2023-01-01T10:00:00Z',  # UTC time
                'state': 'closed',  # Again, using 'closed' as the state
                'events': [event_data_2]
            })
        ]

    @patch('data_loader.DataLoader.get_issues')
    def test_response_time(self, mock_get_issues):
        mock_get_issues.return_value = self.mock_issues
        analysis = IssueResponseTimeAnalysis()

        created_date_issue_1 = self.mock_issues[0].created_date
        event_date_issue_1 = self.mock_issues[0].events[1].event_date

        response_time_issue_1 = (event_date_issue_1 - created_date_issue_1).days

        try:
            analysis.run()
            self.assertEqual(response_time_issue_1, 1)  
        except Exception as e:
            raise AssertionError(f"Unexpected error calculating response time: {e}")

    @patch('data_loader.DataLoader.get_issues')
    def test_reponse_time_2(self, mock_get_issues):
        mock_get_issues.return_value = self.mock_issues
        analysis = IssueResponseTimeAnalysis()

        created_date_issue_2 = self.mock_issues[1].created_date
        event_date_issue_2 = self.mock_issues[1].events[0].event_date

        response_time_issue_2 = (event_date_issue_2 - created_date_issue_2).days

        try:
            analysis.run()
            self.assertEqual(response_time_issue_2, 1)  
        except Exception as e:
            raise AssertionError(f"Unexpected error calculating response time: {e}")

    @patch('data_loader.DataLoader.get_issues')
    def test_calc_average_time(self, mock_get_issues):
        mock_get_issues.return_value = self.mock_issues
        analysis = IssueResponseTimeAnalysis()

        created_date_issue_1 = self.mock_issues[0].created_date
        event_date_issue_1 = self.mock_issues[0].events[1].event_date
        created_date_issue_2 = self.mock_issues[1].created_date
        event_date_issue_2 = self.mock_issues[1].events[0].event_date

        response_time_issue_1 = (event_date_issue_1 - created_date_issue_1).days
        response_time_issue_2 = (event_date_issue_2 - created_date_issue_2).days

        response_times = [response_time_issue_1, response_time_issue_2]
        avg_response_time = sum(response_times) / len(response_times)

        try:
            analysis.run()
            self.assertEqual(avg_response_time, 1.0)  
        except Exception as e:
            raise AssertionError(f"Unexpected error calculating average time: {e}")

    @patch('data_loader.DataLoader.get_issues')
    def test_calc_min_time(self, mock_get_issues):
        mock_get_issues.return_value = self.mock_issues
        analysis = IssueResponseTimeAnalysis()

        created_date_issue_1 = self.mock_issues[0].created_date
        event_date_issue_1 = self.mock_issues[0].events[1].event_date
        created_date_issue_2 = self.mock_issues[1].created_date
        event_date_issue_2 = self.mock_issues[1].events[0].event_date

        response_time_issue_1 = (event_date_issue_1 - created_date_issue_1).days
        response_time_issue_2 = (event_date_issue_2 - created_date_issue_2).days

        response_times = [response_time_issue_1, response_time_issue_2]
        min_response_time = min(response_times)

        try:
            analysis.run()
            self.assertEqual(min_response_time, 1) 
        except Exception as e:
            raise AssertionError(f"Unexpected error calculating minimum time: {e}")

    @patch('data_loader.DataLoader.get_issues')
    def test_calc_max_time(self, mock_get_issues):
        mock_get_issues.return_value = self.mock_issues
        analysis = IssueResponseTimeAnalysis()

        created_date_issue_1 = self.mock_issues[0].created_date
        event_date_issue_1 = self.mock_issues[0].events[1].event_date
        created_date_issue_2 = self.mock_issues[1].created_date
        event_date_issue_2 = self.mock_issues[1].events[0].event_date

        response_time_issue_1 = (event_date_issue_1 - created_date_issue_1).days
        response_time_issue_2 = (event_date_issue_2 - created_date_issue_2).days

        response_times = [response_time_issue_1, response_time_issue_2]
        min_response_time = min(response_times)

        try:
            analysis.run()
            self.assertEqual(max_response_time, 1) 
        except Exception as e:
            raise AssertionError(f"Unexpected error calculating maximum time: {e}")

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
