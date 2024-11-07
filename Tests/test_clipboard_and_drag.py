import unittest
from unittest.mock import patch, MagicMock
import pyperclip
import time
from ClipboardAndDragProtection.clipboard_manager import ClipboardManager

class TestClipboardAndDrag(unittest.TestCase):
    def setUp(self):
        # Instantiate ClipboardManager for use in tests
        self.clipboard_manager = ClipboardManager()

    @patch('pyperclip.paste')
    @patch('pyperclip.copy')
    def test_monitor_clipboard_content_cleared(self, mock_copy, mock_paste):
        # Mock the paste to simulate clipboard content
        mock_paste.side_effect = ["Test Content", "Test Content", ""]
        # Mock the copy to simulate clearing the clipboard
        mock_copy.return_value = None

        # Run the clipboard monitoring in a loop for a limited time
        with patch('time.sleep', return_value=None):
            for _ in range(3):
                self.clipboard_manager.monitor_clipboard()

        # Check if clipboard was cleared by calling pyperclip.copy('')
        self.assertEqual(mock_copy.call_count, 1)
        mock_copy.assert_called_with('')

    @patch('pyperclip.paste')
    def test_monitor_clipboard_no_change(self, mock_paste):
        # Mock the paste to always return the same content
        mock_paste.return_value = "Same Content"

        # Run the clipboard monitoring in a loop for a limited time
        with patch('time.sleep', return_value=None):
            for _ in range(3):
                self.clipboard_manager.monitor_clipboard()

        # Ensure that clipboard clearing (pyperclip.copy) was never called
        with patch('pyperclip.copy') as mock_copy:
            mock_copy.assert_not_called()

if __name__ == '__main__':
    unittest.main()
