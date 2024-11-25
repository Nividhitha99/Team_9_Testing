import unittest
from unittest.mock import patch, MagicMock
from top_commenters_vs_creators_analysis import TopCommentersVsCreatorsAnalysis

class TestTopCommentersVsCreatorsAnalysis(unittest.TestCase):

    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_no_issues_loaded(self, mock_get_issues):
        """Test Case 1: No issues are loaded"""
        # simulate as no issues are loaded
        mock_get_issues.return_value = []
        # since no issues were loaded, the code fails at line 52 in TopCommentersVsCreatorsAnalysis
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verify no plot is shown
            mock_show.assert_not_called()

    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_issues_with_no_events(self, mock_get_issues):
        """Test Case 2: Issues with no events"""
        # simulate mock issues with no events
        mock_get_issues.return_value = [
            MagicMock(creator="user1", events=[])
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verify no plot is shown
            mock_show.assert_not_called()

    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_issues_with_events_no_comments(self, mock_get_issues):
        """Test Case 3: Issues with events but no comments"""
        # simulate mock issues with no comments label
        mock_get_issues.return_value = [
            MagicMock(creator="user1", events=[MagicMock(event_type="labeled", author="user2")])
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is shown twice
            assert mock_show.call_count == 2
            
    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_issues_with_comments_none_creator(self, mock_get_issues):
        """Test Case 4: Issues with comments but None creator"""
        # simulate mock issues with comments label and creator set to None type
        mock_get_issues.return_value = [
            MagicMock(creator=None, events=[MagicMock(event_type="commented", author="user2")])
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            try:
                analysis.run()
                # Verify no plot is shown
                mock_show.assert_not_called()
            except Exception as e:
                self.fail(f"Test Case 4 failed: {e}")
            
    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_issues_with_creator_no_comments(self, mock_get_issues):
        """Test Case 5: Issues with creator but No comments"""
        # simulate mock issues with no comments label
        mock_get_issues.return_value = [
            MagicMock(creator="user1", events=[MagicMock(event_type="labeled", author="user2")])
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is shown twice
            assert mock_show.call_count == 2
            
    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_multiple_creators_and_commenters(self, mock_get_issues):
        """Test Case 6: Multiple Creators and Commenters"""
        # simulate mock issues with Multiple Creators and Commenters
        mock_get_issues.return_value = [
            MagicMock(creator="user1", events=[MagicMock(event_type="commented", author="user2")]),
            MagicMock(creator="user1", events=[MagicMock(event_type="commented", author="user1")]),
            MagicMock(creator="user2", events=[MagicMock(event_type="commented", author="user4")]),
            MagicMock(creator="user3", events=[MagicMock(event_type="commented", author="user9")]),
            MagicMock(creator="user4", events=[MagicMock(event_type="commented", author="user1")])
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is shown twice
            assert mock_show.call_count == 2

    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_more_than_10_creators_and_commenters(self, mock_get_issues):
        """Test Case 7: more than 10 creators or commenters"""
        # simulate mock issues with more than 10 creators or commenters
        mock_get_issues.return_value = [
            MagicMock(creator=f"user{i}", events=[MagicMock(event_type="commented", author=f"user{j}")])
            for i in range(15) for j in range(2)
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            # Verifying plot is shown twice
            assert mock_show.call_count == 2

    @patch('top_commenters_vs_creators_analysis.DataLoader.get_issues')
    def test_invalid_data(self, mock_get_issues):
        """Test Case 8: Invalid Data"""
        # simulate mock issues with none data for commenters and creators
        mock_get_issues.return_value = [
            MagicMock(creator=None, events=[MagicMock(event_type="commented", author=None)])
        ]
        analysis = TopCommentersVsCreatorsAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            try:
                analysis.run()
                # Verify no plot is shown
                mock_show.assert_not_called()
            except Exception as e:
                self.fail(f"Test Case 8: Failed. Invalid Data: {e}")
   

if __name__ == "__main__":
    unittest.main()
