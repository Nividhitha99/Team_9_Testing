import unittest
from collections import Counter
from analysis.label_analysis import analyze_issue_labels
from unittest.mock import patch
from visualizations.plot_labels import plot_label_distribution


class TestLabelAnalysis(unittest.TestCase):
    def test_analyze_with_no_issues(self):
        """Test analyze_issue_labels with no issues."""
        issues = []
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_no_labels(self):
        """Test analyze_issue_labels when issues have no labels."""
        issues = [{"id": 1, "labels": []}, {"id": 2, "labels": []}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_single_label_per_issue(self):
        """Test analyze_issue_labels with one label per issue."""
        issues = [{"id": 1, "labels": ["bug"]}, {"id": 2, "labels": ["feature"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_multiple_labels_per_issue(self):
        """Test analyze_issue_labels with multiple labels per issue."""
        issues = [
            {"id": 1, "labels": ["bug", "urgent"]},
            {"id": 2, "labels": ["feature", "low-priority"]},
        ]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "urgent": 1, "feature": 1, "low-priority": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_duplicate_labels_in_issues(self):
        """Test analyze_issue_labels with duplicate labels within a single issue."""
        issues = [{"id": 1, "labels": ["bug", "bug", "urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 2, "urgent": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_duplicate_labels_across_issues(self):
        """Test analyze_issue_labels with duplicate labels across multiple issues."""
        issues = [
            {"id": 1, "labels": ["bug", "urgent"]},
            {"id": 2, "labels": ["bug", "feature"]},
        ]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 2, "urgent": 1, "feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_missing_labels_key(self):
        """Test analyze_issue_labels when the 'labels' key is missing in some issues."""
        issues = [{"id": 1}, {"id": 2, "labels": ["feature"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_empty_issues(self):
        """Test analyze_issue_labels when issues contain empty dictionaries."""
        issues = [{}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_non_string_labels(self):
        """Test analyze_issue_labels when labels contain non-string values."""
        issues = [{"id": 1, "labels": ["bug", 123, None, "urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "urgent": 1, 123: 1, None: 1})
        self.assertEqual(result, expected)


    def test_analyze_with_no_issues(self):
        """Test analyze_issue_labels with no issues."""
        issues = []
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_no_labels(self):
        """Test analyze_issue_labels when issues have no labels."""
        issues = [{"id": 1, "labels": []}, {"id": 2, "labels": []}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_missing_labels_key(self):
        """Test analyze_issue_labels when the 'labels' key is missing in some issues."""
        issues = [{"id": 1}, {"id": 2, "labels": ["feature"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_empty_labels(self):
        """Test analyze_issue_labels when labels are explicitly empty."""
        issues = [{"id": 1, "labels": []}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_duplicate_labels_in_one_issue(self):
        """Test analyze_issue_labels with duplicate labels in a single issue."""
        issues = [{"id": 1, "labels": ["bug", "bug", "urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 2, "urgent": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_duplicate_labels_across_multiple_issues(self):
        """Test analyze_issue_labels with duplicate labels across multiple issues."""
        issues = [
            {"id": 1, "labels": ["bug", "urgent"]},
            {"id": 2, "labels": ["bug", "feature"]},
        ]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 2, "urgent": 1, "feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_case_sensitive_labels(self):
        """Test analyze_issue_labels with case-sensitive labels."""
        issues = [{"id": 1, "labels": ["bug", "Bug", "BUG"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "Bug": 1, "BUG": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_non_string_labels(self):
        """Test analyze_issue_labels with non-string labels."""
        issues = [{"id": 1, "labels": ["bug", 123, None, "urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "urgent": 1, 123: 1, None: 1})
        self.assertEqual(result, expected)

    def test_analyze_with_special_characters_in_labels(self):
        """Test analyze_issue_labels with labels containing special characters."""
        issues = [{"id": 1, "labels": ["bug!", "@urgent", "#feature"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug!": 1, "@urgent": 1, "#feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_empty_issues(self):
        """Test analyze_issue_labels when issues contain empty dictionaries."""
        issues = [{}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_large_number_of_issues(self):
        """Test analyze_issue_labels with a large number of issues."""
        issues = [{"id": i, "labels": ["bug"]} for i in range(10000)]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 10000})
        self.assertEqual(result, expected)

    def test_analyze_with_nested_labels(self):
        """Test analyze_issue_labels when labels are nested lists (invalid format)."""
        issues = [{"id": 1, "labels": [["bug", "urgent"]]}]
        with self.assertRaises(TypeError):
            analyze_issue_labels(issues)

    def test_analyze_with_mixed_data_types_in_issues(self):
        """Test analyze_issue_labels with mixed data types in the issues list."""
        issues = [
            {"id": 1, "labels": ["bug", "urgent"]},
            {"id": 2, "labels": "feature"},  # Invalid: string instead of list
            {"id": 3, "labels": None},  # Invalid: None instead of list
            {"id": 4},  # Missing 'labels' key
            {},  # Empty issue
        ]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "urgent": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_labels_containing_numbers_as_strings(self):
        """Test analyze_issue_labels with labels that are numbers but as strings."""
        issues = [{"id": 1, "labels": ["123", "456", "bug"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"123": 1, "456": 1, "bug": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_duplicate_and_case_insensitive_labels(self):
        """Test analyze_issue_labels with duplicate labels and case variations."""
        issues = [
            {"id": 1, "labels": ["Bug", "bug", "BUG", "feature"]},
            {"id": 2, "labels": ["feature", "FEATURE"]},
        ]
        result = analyze_issue_labels(issues)
        expected = Counter(
            {"Bug": 1, "bug": 1, "BUG": 1, "feature": 2, "FEATURE": 1}
        )
        self.assertEqual(result, expected)





    def test_analyze_with_all_empty_labels(self):
        """Test analyze_issue_labels where all issues have empty labels."""
        issues = [{"id": 1, "labels": []}, {"id": 2, "labels": []}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_special_characters_and_spaces_in_labels(self):
        """Test analyze_issue_labels with labels containing spaces and special characters."""
        issues = [{"id": 1, "labels": ["bug ", " high-priority", "!urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug ": 1, " high-priority": 1, "!urgent": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_large_labels(self):
        """Test analyze_issue_labels with extremely large labels."""
        issues = [{"id": 1, "labels": ["a" * 1000, "b" * 2000]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"a" * 1000: 1, "b" * 2000: 1})
        self.assertEqual(result, expected)

    def test_analyze_with_nested_issues(self):
        """Test analyze_issue_labels where issues contain nested dictionaries."""
        issues = [
            {"id": 1, "labels": ["bug", "urgent"], "extra": {"priority": "high"}},
            {"id": 2, "labels": ["feature"], "extra": {"priority": "low"}},
        ]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "urgent": 1, "feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_non_iterable_labels(self):
        """Test analyze_issue_labels where labels is a non-iterable (invalid format)."""
        issues = [{"id": 1, "labels": "not-a-list"}]  # Labels as string instead of list

        try:
            analyze_issue_labels(issues)
        except TypeError as e:
            raise AssertionError(f"TypeError encountered: {e}")  # Treat TypeError as AssertionError

       
        self.fail("Expected TypeError was not raised.")




    def test_analyze_with_labels_as_empty_strings(self):
        """Test analyze_issue_labels where labels contain empty strings."""
        issues = [{"id": 1, "labels": ["", "bug", "urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"": 1, "bug": 1, "urgent": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_labels_as_whitespace(self):
        """Test analyze_issue_labels where labels contain only whitespace."""
        issues = [{"id": 1, "labels": [" ", "   ", "bug"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({" ": 1, "   ": 1, "bug": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_unicode_characters_in_labels(self):
        """Test analyze_issue_labels with labels containing Unicode characters."""
        issues = [{"id": 1, "labels": ["🔥bug", "feature✓", "🚀urgent"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"🔥bug": 1, "feature✓": 1, "🚀urgent": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_labels_as_boolean_values(self):
        """Test analyze_issue_labels where labels contain boolean values."""
        issues = [{"id": 1, "labels": ["bug", True, False]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, True: 1, False: 1})
        self.assertEqual(result, expected)

    def test_analyze_with_labels_as_mixed_data_structures(self):
        """Test analyze_issue_labels where labels contain mixed data structures."""
        issues = [{"id": 1, "labels": ["bug", 123, {"key": "value"}, [1, 2, 3]]}]
        with self.assertRaises(TypeError):
            analyze_issue_labels(issues)

    def test_analyze_with_labels_having_duplicate_entries_in_multiple_issues(self):
        """Test analyze_issue_labels with labels repeating across issues."""
        issues = [
            {"id": 1, "labels": ["bug", "urgent"]},
            {"id": 2, "labels": ["bug", "urgent"]},
            {"id": 3, "labels": ["feature", "bug"]},
        ]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 3, "urgent": 2, "feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_labels_as_numbers(self):
        """Test analyze_issue_labels where labels are purely numeric."""
        issues = [{"id": 1, "labels": [123, 456, 789]}]
        result = analyze_issue_labels(issues)
        expected = Counter({123: 1, 456: 1, 789: 1})
        self.assertEqual(result, expected)

    def test_analyze_with_duplicate_labels_in_same_issue(self):
        """Test analyze_issue_labels where the same label is repeated within a single issue."""
        issues = [{"id": 1, "labels": ["bug", "bug", "bug"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 3})
        self.assertEqual(result, expected)

    def test_analyze_with_empty_issues_list(self):
        """Test analyze_issue_labels with an empty issues list."""
        issues = []
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_large_number_of_duplicates(self):
        """Test analyze_issue_labels where all issues have the same label."""
        issues = [{"id": i, "labels": ["bug"]} for i in range(10000)]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 10000})
        self.assertEqual(result, expected)


    def test_analyze_with_no_issues(self):
        """Test analyze_issue_labels with no issues."""
        issues = []
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_no_labels(self):
        """Test analyze_issue_labels when issues have no labels."""
        issues = [{"id": 1, "labels": []}, {"id": 2, "labels": []}]
        result = analyze_issue_labels(issues)
        self.assertEqual(result, Counter())

    def test_analyze_with_single_label_per_issue(self):
        """Test analyze_issue_labels with one label per issue."""
        issues = [{"id": 1, "labels": ["bug"]}, {"id": 2, "labels": ["feature"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug": 1, "feature": 1})
        self.assertEqual(result, expected)

    def test_analyze_with_large_number_of_labels(self):
        """Test analyze_issue_labels with a large number of labels."""
        issues = [{"id": i, "labels": ["label_{}".format(i)]} for i in range(1, 101)]
        result = analyze_issue_labels(issues)
        expected = Counter({"label_{}".format(i): 1 for i in range(1, 101)})
        self.assertEqual(result, expected)

    def test_analyze_with_special_characters_in_labels(self):
        """Test analyze_issue_labels with labels containing special characters."""
        issues = [{"id": 1, "labels": ["bug!", "@urgent", "#feature"]}]
        result = analyze_issue_labels(issues)
        expected = Counter({"bug!": 1, "@urgent": 1, "#feature": 1})
        self.assertEqual(result, expected)

    @patch("visualizations.plot_labels.plt.show")
    @patch("visualizations.plot_labels.plt.bar")
    def test_plot_with_valid_data(self, mock_bar, mock_show):
        """Test plot_label_distribution with valid label data."""
        label_counts = Counter({"bug": 10, "feature": 5, "urgent": 2})

        try:
            plot_label_distribution(label_counts)
        except ValueError as e:
            raise AssertionError(f"ValueError encountered: {e}")  # Treat ValueError as AssertionError

        # Ensure bar chart is called with expected arguments
        mock_bar.assert_called_once_with(("bug", "feature", "urgent"), (10, 5, 2), color="skyblue")
        mock_show.assert_called_once()



    @patch("visualizations.plot_labels.plt.show")
    def test_plot_with_empty_data(self, mock_show):
        """Test plot_label_distribution with empty label data."""
        label_counts = Counter()

        try:
            plot_label_distribution(label_counts)
        except ValueError as e:
            raise AssertionError(f"ValueError encountered: {e}")  # Treat ValueError as AssertionError

        # Ensure plt.show() is NOT called
        mock_show.assert_not_called()

    @patch("visualizations.plot_labels.plt.show")
    @patch("visualizations.plot_labels.plt.bar")
    def test_plot_with_special_characters(self, mock_bar, mock_show):
        """Test plot_label_distribution with labels containing special characters."""
        label_counts = Counter({"bug!": 5, "@urgent": 3, "#feature": 8})
        plot_label_distribution(label_counts)

        # Ensure bar chart and show() were called
        mock_bar.assert_called_once()
        mock_show.assert_called_once()

    @patch("visualizations.plot_labels.plt.show")
    @patch("visualizations.plot_labels.plt.bar")
    def test_plot_with_large_number_of_labels(self, mock_bar, mock_show):
        """Test plot_label_distribution with a large number of labels."""
        label_counts = Counter({f"label_{i}": i for i in range(1, 101)})
        plot_label_distribution(label_counts)

        # Ensure bar chart and show() were called
        mock_bar.assert_called_once()
        mock_show.assert_called_once()

    @patch("visualizations.plot_labels.plt.show")
    @patch("visualizations.plot_labels.plt.bar")
    def test_plot_with_single_label(self, mock_bar, mock_show):
        """Test plot_label_distribution with a single label."""
        label_counts = Counter({"bug": 1})

        try:
            plot_label_distribution(label_counts)
        except ValueError as e:
            raise AssertionError(f"ValueError encountered: {e}")  # Treat ValueError as AssertionError

        # Ensure bar chart is called with expected arguments
        mock_bar.assert_called_once_with(("bug",), (1,), color="skyblue")
        mock_show.assert_called_once()







if __name__ == "__main__":
    unittest.main()
