from __future__ import absolute_import

import fnmatch
import os
import unittest

from . import validate_json_format


class TestSettings(unittest.TestCase):
    def _get_json_files(self, file_pattern, folder='.'):
        """
        Recursively yield file paths matching the given pattern within the specified folder.
        """
        for root, dirnames, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, file_pattern):
                yield os.path.join(root, filename)
            for dirname in [d for d in dirnames
                            if d not in (
                                '.cache',
                                '.git',
                                '.github',
                                '.idea',
                                'jsprettier',
                                'messages',
                                'node_modules',
                                'screenshots',
                                'scripts',
                                'Snippets',
                                'tests',
                                'venv',
                                os.path.join('tests', '__pycache__')
                            )]:
                for f in self._get_json_files(file_pattern, os.path.join(root, dirname)):
                    yield f

    def test_json_settings(self):
        """
        Test each JSON file to ensure it conforms to the expected format.
        """
        file_patterns = (
            '*.sublime-commands',
            '*.sublime-menu',
            '*.sublime-settings'
        )
        for file_pattern in file_patterns:
            for f in self._get_json_files(file_pattern):
                print(f)
                self.assertFalse(validate_json_format.CheckJsonFormat(False, True).check_format(f),
                                 "%s does not conform to expected format." % f)
