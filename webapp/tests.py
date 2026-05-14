from django.test import TestCase
from unittest.mock import MagicMock, patch
from pathlib import Path
from webapp.tasks import _robust_delete
import io
from contextlib import redirect_stdout

class RobustDeleteTests(TestCase):
    def test_delete_success(self):
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True

        _robust_delete(mock_path)

        mock_path.exists.assert_called_once()
        mock_path.unlink.assert_called_once()

    def test_delete_not_exists(self):
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False

        _robust_delete(mock_path)

        mock_path.exists.assert_called_once()
        mock_path.unlink.assert_not_called()

    @patch('webapp.tasks.time.sleep', return_value=None)
    def test_delete_retry_success(self, mock_sleep):
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        # First call raises PermissionError, second succeeds
        mock_path.unlink.side_effect = [PermissionError, None]

        _robust_delete(mock_path, retries=3, delay=0.1)

        self.assertEqual(mock_path.unlink.call_count, 2)
        mock_sleep.assert_called_once_with(0.1)

    @patch('webapp.tasks.time.sleep', return_value=None)
    def test_delete_max_retries_reached(self, mock_sleep):
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.unlink.side_effect = PermissionError

        f = io.StringIO()
        with redirect_stdout(f):
            _robust_delete(mock_path, retries=3, delay=0.1)

        self.assertEqual(mock_path.unlink.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        self.assertIn("Warning: Could not delete temporary file", f.getvalue())

    def test_delete_unexpected_exception(self):
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.unlink.side_effect = Exception("Unexpected")

        f = io.StringIO()
        with redirect_stdout(f):
            _robust_delete(mock_path)

        mock_path.unlink.assert_called_once()
        self.assertIn("Warning: An unexpected error occurred while deleting", f.getvalue())
