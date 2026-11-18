"""Synthetic package checks using source exports outside the working tree."""
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from check_package import REQUIRED, check


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        temporary = Path(self.tmp.name)
        self.root = temporary / 'source'
        self.root.mkdir()
        self.outside = temporary / 'outside'
        self.outside.mkdir()
        (self.outside / 'marker.txt').write_text('synthetic fixture\n')
        source = Path(__file__).resolve().parent.parent
        for name in REQUIRED | {'scripts/test_check_package.py'}:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)

    def symlink(self, name, target, directory=False):
        try:
            (self.root / name).symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as error:
            if os.name == 'nt':
                self.skipTest('Symlink creation is unavailable: ' + str(error))
            raise

    def assert_rejected_symlink(self, name):
        errors, _ = check(self.root)
        self.assertTrue(any('symlink' in error and name in error for error in errors), errors)

    def test_valid_source_export(self):
        self.assertEqual(check(self.root)[0], [])

    def test_external_directory_symlink_is_rejected(self):
        self.symlink('linked-directory', self.outside, directory=True)
        self.assert_rejected_symlink('linked-directory')

    def test_internal_directory_symlink_is_rejected(self):
        self.symlink('linked-directory', self.root / 'assets', directory=True)
        self.assert_rejected_symlink('linked-directory')

    def test_broken_directory_symlink_is_rejected(self):
        self.symlink('linked-directory', self.outside / 'missing', directory=True)
        self.assert_rejected_symlink('linked-directory')

    def test_file_symlink_is_rejected(self):
        self.symlink('linked-file.txt', self.outside / 'marker.txt')
        self.assert_rejected_symlink('linked-file.txt')


if __name__ == '__main__':
    unittest.main()
