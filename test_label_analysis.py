import unittest
from unittest.mock import patch
from label_analysis import LabelAnalysis
from model import Issue

class TestLabelAnalysis(unittest.TestCase):

    @patch('label_analysis.DataLoader.get_issues')
    def test_no_issues_loaded(self, mock_get_issues):
        """Test Case 1: No issues are loaded"""
        # simulate as no issues are loaded
        mock_get_issues.return_value = []
        # since no issues were loaded, the code fails at line 39 in label_analysis.py
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            try:
                analysis.run()
                # Verifying no plot is saved
                mock_show.assert_not_called()
            except KeyError as e:
                self.fail(f"Test Case 1: Test failed due to a KeyError: {e}")
            except Exception as e:
                self.fail(f"Test Case 1: Test failed due to an exception: {e}")
        
    @patch('label_analysis.DataLoader.get_issues')
    def test_issues_without_labels(self, mock_get_issues):
        """Test Case 2: Issues without Labels"""
        # simulate mock issues without lables
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": [],
                "state": "closed",
                "title": "Test Case 2: Testing no lables loaded",
                "text": "Test Case 2_text: Testing no lables loaded",
                "number": 2,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        mock_get_issues.return_value = mockIssues
        # since the labels are empty, the code fails at line 58 while creating and concatenating the object
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            try:
                analysis.run()
                # Verifying no plot is saved
                mock_savefig.assert_not_called()
            except KeyError as e:
                self.fail(f"Test Case 2: Test failed due to a KeyError: {e}")
            except Exception as e:
                self.fail(f"Test Case 2: Test failed due to an exception: {e}")

    @patch('label_analysis.DataLoader.get_issues')
    def test_issues_with_labels_None_datatype(self, mock_get_issues):
        """Test Case 3: Issues with none datatype Labels"""
        # simulate mock issues with None datatype label
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": None,
                "state": "closed",
                "title": "Test Case 3: Testing none datatype lables",
                "text": "Test Case 3_text: Testing none datatype lables",
                "number": 2,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        mock_get_issues.return_value = mockIssues
        # since the labels are set to None datatype, the code fails at line 58 while creating and concatenating the object
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            try:
                analysis.run()
                # Verifying no plot is saved
                mock_savefig.assert_not_called()
            except KeyError as e:
                self.fail(f"Test Case 3: Test failed due to a KeyError: {e}")
            except Exception as e:
                self.fail(f"Test Case 3: Test failed due to an exception: {e}")

    @patch('label_analysis.DataLoader.get_issues')
    def test_issues_with_labels_mixed_states(self, mock_get_issues):
        """Test Case 4: Issues with mixed states: Open and Closed"""
        # simulate a mock issue with two mixed states
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug"],
                "state": "closed",
                "title": "Test Case 4: Testing with mixed states open and closed",
                "text": "Test Case 4_text: Testing with mixed states open and closed",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug"],
                "state": "open",
                "title": "Test Case 4: Testing with mixed states open and closed",
                "text": "Test Case 4_text: Testing with mixed states open and closed",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        mock_get_issues.return_value = mockIssues
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying the plot is saved
            mock_show.assert_called_once()

    @patch('label_analysis.DataLoader.get_issues')
    def test_issues_with_labels_different_years(self, mock_get_issues):
        """Test Case 5: same issues created in two different years"""
        # simulate the issue with two different years 
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug"],
                "state": "closed",
                "title": "Test Case 5: Issues created and updated in different years",
                "text": "Test Case 5_text: Issues created and updated in different years",
                "number": 1,
                "created_date": "2023-10-20T00:33:06+00:00",
                "updated_date": "2023-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug"],
                "state": "open",
                "title": "Test Case 5: Issues created and updated in different years",
                "text": "Test Case 5_text: Issues created and updated in different years",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        mock_get_issues.return_value = mockIssues
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is saved
            mock_show.assert_called_once()

    @patch('label_analysis.DataLoader.get_issues')
    def test_less_than_three_labels(self, mock_get_issues):
        """Test Case 6: Issues with less than 3 labels"""
        # simulate the issues with only two labels
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug","status/triage"],
                "state": "closed",
                "title": "Test Case 6: Testing issues with only two labels",
                "text": "Test Case 6_text: Testing issues with only two labels",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9786",
                "creator": "dbrtly",
                "labels": ["kind/triage","status/duplicate"],
                "state": "closed",
                "title": "Test Case 6: Testing issues with only two labels",
                "text": "Test Case 6_text: Testing issues with only two labels",
                "number": 2,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        
        mock_get_issues.return_value = mockIssues
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is saved
            mock_show.assert_called_once()

    @patch('label_analysis.DataLoader.get_issues')
    def test_more_than_three_labels(self, mock_get_issues):
        """Test Case 7: More than three labels"""
        # simulate the issues with more than 3 labels
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9784",
                "creator": "dbrtly",
                "labels": ["kind/bug","status/triage"],
                "state": "closed",
                "title": "Test Case 7: Testing issues with more than 3 labels",
                "text": "Test Case 7_text: Testing issues with more than 3 labels",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly2",
                "labels": ["kind/triage","status/duplicate"],
                "state": "closed",
                "title": "Test Case 7: Testing issues with more than 3 labels",
                "text": "Test Case 7_text: Testing issues with more than 3 labels",
                "number": 2,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9786",
                "creator": "dbrtly3",
                "labels": ["kind/bug","area/docs"],
                "state": "closed",
                "title": "Test Case 7: Testing issues with more than 3 labels",
                "text": "Test Case 7_text: Testing issues with more than 3 labels",
                "number": 3,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9787",
                "creator": "dbrtly4",
                "labels": ["kind/feature","status/duplicate"],
                "state": "closed",
                "title": "Test Case 7: Testing issues with more than 3 labels",
                "text": "Test Case 7_text: Testing issues with more than 3 labels",
                "number": 4,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
        ]
        mock_get_issues.return_value = mockIssues

        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is saved
            mock_show.assert_called_once()

    @patch('label_analysis.DataLoader.get_issues')
    def test_issues_with_no_closed_state(self, mock_get_issues):
        """Test Case 8: Issues with no closed state"""
        # simulate mock issues with no closed state
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug"],
                "state": "open",
                "title": "Test Case 8: Testing issues with no closed state",
                "text": "Test Case 8_text: Testing issues with no closed state",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9786",
                "creator": "dbrtly2",
                "labels": ["kind/triage"],
                "state": "open",
                "title": "Test Case 8: Testing issues with no closed state",
                "text": "Test Case 8_text: Testing issues with no closed state",
                "number": 2,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        
        mock_get_issues.return_value = mockIssues
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verify no plot is saved
            mock_show.assert_called_once()
            
    @patch('label_analysis.DataLoader.get_issues')
    def test_issues_with_no_open_state(self, mock_get_issues):
        """Test Case 9: Issues with no open state"""
        # simulate mock issues with no open state 
        mockIssues = [
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9785",
                "creator": "dbrtly",
                "labels": ["kind/bug"],
                "state": "closed",
                "title": "Test Case 9: Testing issues with no open state",
                "text": "Test Case 9_text: Testing issues with no open state",
                "number": 1,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            }),
            Issue({
                "url": "https://github.com/python-poetry/poetry/issues/9786",
                "creator": "dbrtly2",
                "labels": ["kind/triage"],
                "state": "closed",
                "title": "Test Case 9: Testing issues with no open state",
                "text": "Test Case 9_text: Testing issues with no open state",
                "number": 2,
                "created_date": "2024-10-20T00:33:06+00:00",
                "updated_date": "2024-10-20T08:00:46+00:00"
            })
        ]
        
        mock_get_issues.return_value = mockIssues
        analysis = LabelAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying no plot is saved
            mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
