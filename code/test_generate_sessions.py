"""Regression tests for authoring errors and generated resource links."""
import tempfile
import unittest
from pathlib import Path

from generate_sessions import generate, read_event, render


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'programming-club' / '2026-01-01-example'
        self.folder.mkdir(parents=True)
        self.path = self.folder / 'event.yml'
        self.base = 'title: "A | B < C"\nauthor: "Someone"\ndate: 2026-01-01\n'

    def write(self, extra=''):
        self.path.write_text(self.base + extra)
        return read_event(self.path, 'programming-club', self.root)

    def test_multiple_resources_and_nested_local_files(self):
        (self.folder / 'data').mkdir()
        (self.folder / 'data' / 'notes file.txt').write_text('notes')
        self.write('resources:\n  - path: data/notes file.txt\n    label: Notes\n  - url: https://example.org/demo?a=1&b=2\n    label: Demo\n')
        generate(self.root, ['programming-club'])
        output = self.root / 'docs/sessions/programming-club'
        self.assertTrue((output / self.folder.name / 'data/notes file.txt').is_file())
        page = (output / 'index.md').read_text()
        self.assertIn('A &#124; B &lt; C', page)
        self.assertIn('notes%20file.txt', page)
        self.assertIn('a=1&b=2', page)

    def test_legacy_colab_is_closed_and_linked(self):
        event = self.write('repositories:\n  location: colab\n  name: Demo\n  url: https://colab.research.google.com/demo\n')
        page = render('programming-club', [event])
        self.assertEqual(page.count('](https://colab.research.google.com/demo)'), 2)
        self.assertIn('Open in Colab', page)

    def test_draft_with_unfinished_metadata(self):
        self.path.write_text('status: draft\ntitle: ...\n')
        self.assertIsNone(read_event(self.path, 'programming-club', self.root))

    def test_bad_inputs(self):
        for extra in ('resources: invalid\n', 'resources:\n  - url: javascript:alert(1)\n', 'resources:\n  - path: ../secret\n', 'resources:\n  - path: missing.ipynb\n', 'resources:\n  - url: https://example.org\n    path: notes.txt\n'):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.write(extra)
        self.path.write_text('[]')
        with self.assertRaises(ValueError):
            read_event(self.path, 'programming-club', self.root)

    def test_validation_failure_does_not_write_any_pages(self):
        self.write()
        other = self.root / 'talks' / 'broken'
        other.mkdir(parents=True)
        (other / 'event.yml').write_text('title: Missing fields')
        with self.assertRaises(ValueError):
            generate(self.root, ['programming-club', 'talks'])
        self.assertFalse((self.root / 'docs').exists())

    def test_check_does_not_write(self):
        self.write()
        generate(self.root, ['programming-club'], check=True)
        self.assertFalse((self.root / 'docs').exists())


if __name__ == '__main__':
    unittest.main()
