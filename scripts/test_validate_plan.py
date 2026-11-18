"""Synthetic checks: python -m unittest discover -s scripts -p 'test_*.py'."""
import tempfile
import unittest
from pathlib import Path
from validate_plan import validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'tasks').mkdir()
        (self.root / 'PROJECT.md').write_text('# Project guide\n\n[Task register](TASKS.md)\n')
        self.task('A', 'none')
        self.task('B', 'A')
        self.register()

    def task(self, ident, deps, status='todo'):
        (self.root / 'tasks' / (ident + '.md')).write_text(
            f'ID: {ident}\nStatus: {status}\nDependencies: {deps}\n')

    def register(self, a_deps='none', a_status='todo'):
        (self.root / 'TASKS.md').write_text(
            '| ID | Task | Status | Dependencies | File |\n'
            '|---|---|---|---|---|\n'
            f'| A | First | {a_status} | {a_deps} | [A](tasks/A.md) |\n'
            '| B | Second | todo | A | [B](tasks/B.md) |\n')

    def test_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_metadata_examples_in_fenced_code(self):
        examples = (
            '```text\nID: EXAMPLE\nStatus: done\nDependencies: none\n```\n',
            '~~~yaml\nID: EXAMPLE\nStatus: done\nDependencies: none\n~~~\n',
            '````text\n```\nID: EXAMPLE\nStatus: done\nDependencies: none\n```\n````\n',
        )
        for example in examples:
            with self.subTest(example=example):
                self.task('A', 'none')
                path = self.root / 'tasks' / 'A.md'
                path.write_text(path.read_text() + '\n## Acceptance\n\n' + example)
                self.assertEqual(validate(self.root), [])

    def test_duplicate_metadata_outside_fences_is_rejected(self):
        path = self.root / 'tasks' / 'A.md'
        path.write_text(path.read_text() + 'ID: SECOND\n')
        self.assertTrue(any('expected one ID field' in error for error in validate(self.root)))

    def test_blank_dependencies_do_not_consume_following_content(self):
        endings = ('\nOwner: worker\n', '\n\nOwner: worker\n', ' \t\n\n## Work\n')
        path = self.root / 'tasks' / 'A.md'
        for ending in endings:
            with self.subTest(ending=ending):
                path.write_text('ID: A\nStatus: todo\nDependencies:' + ending)
                self.assertEqual(validate(self.root), [])

    def test_empty_required_metadata_is_rejected(self):
        path = self.root / 'tasks' / 'A.md'
        original = path.read_text()
        for name, value in (('ID', 'A'), ('Status', 'todo')):
            with self.subTest(field=name):
                path.write_text(original.replace(f'{name}: {value}', f'{name}:'))
                self.assertTrue(validate(self.root))

    def test_fenced_register_without_live_table_is_rejected(self):
        path = self.root / 'TASKS.md'
        table = path.read_text()
        for fence in ('```', '~~~'):
            with self.subTest(fence=fence):
                path.write_text(fence + 'markdown\n' + table + fence + '\n')
                self.assertTrue(validate(self.root))

    def test_register_examples_in_fenced_code_are_ignored(self):
        path = self.root / 'TASKS.md'
        table = path.read_text()
        examples = (
            '```markdown\n' + table + '```\n',
            '~~~markdown\n' + table + '~~~\n',
            '````markdown\n```\n' + table + '```\n````\n',
        )
        for example in examples:
            with self.subTest(example=example):
                path.write_text(table + '\n## Example\n\n' + example)
                self.assertEqual(validate(self.root), [])

    def test_missing_or_invalid_table_separator_is_rejected(self):
        path = self.root / 'TASKS.md'
        original = path.read_text()
        separator = '|---|---|---|---|---|\n'
        replacements = (
            '',
            '|---|---|---|---|\n',
            '|---|---|---|---|---|---|\n',
            '|::---|---|---|---|---|\n',
            '\n' + separator,
        )
        for replacement in replacements:
            with self.subTest(separator=replacement):
                path.write_text(original.replace(separator, replacement))
                self.assertTrue(validate(self.root))

    def test_aligned_table_separator_is_valid(self):
        path = self.root / 'TASKS.md'
        path.write_text(path.read_text().replace(
            '|---|---|---|---|---|', '| :--- | ---: | :---: | --- | --- |'))
        self.assertEqual(validate(self.root), [])

    def test_fenced_block_cannot_join_table_header_and_separator(self):
        path = self.root / 'TASKS.md'
        header, remainder = path.read_text().split('\n', 1)
        path.write_text(header + '\n```text\nExample\n```\n' + remainder)
        self.assertTrue(validate(self.root))

    def test_escaped_pipes_in_task_title(self):
        for backslashes in (1, 3):
            with self.subTest(backslashes=backslashes):
                self.register()
                path = self.root / 'TASKS.md'
                title = 'Support A ' + '\\' * backslashes + '| B \\| C'
                path.write_text(path.read_text().replace('First', title))
                self.assertEqual(validate(self.root), [])

    def test_unescaped_extra_table_delimiter_is_rejected(self):
        for backslashes in (0, 2):
            with self.subTest(backslashes=backslashes):
                self.register()
                path = self.root / 'TASKS.md'
                title = 'Support A ' + '\\' * backslashes + '| B'
                path.write_text(path.read_text().replace('First', title))
                self.assertTrue(any('invalid task table row' in error for error in validate(self.root)))

    def long_chain(self, cycle=False):
        for path in (self.root / 'tasks').iterdir():
            path.unlink()
        rows = ['| ID | Task | Status | Dependencies | File |', '|---|---|---|---|---|']
        count = 1100
        for index in range(count):
            ident = f'T{index:04d}'
            dependency = f'T{index + 1:04d}' if index + 1 < count else ('T0000' if cycle else 'none')
            self.task(ident, dependency)
            rows.append(f'| {ident} | Task | todo | {dependency} | [{ident}](tasks/{ident}.md) |')
        (self.root / 'TASKS.md').write_text('\n'.join(rows) + '\n')

    def test_deep_acyclic_dependency_chain(self):
        self.long_chain()
        try:
            errors = validate(self.root)
        except RecursionError:
            self.fail('A valid deep dependency chain must not exhaust Python recursion.')
        self.assertEqual(errors, [])

    def test_deep_dependency_cycle_is_reported(self):
        self.long_chain(cycle=True)
        try:
            errors = validate(self.root)
        except RecursionError:
            self.fail('A deep dependency cycle must be reported without exhausting Python recursion.')
        self.assertTrue(any('dependency cycle' in error for error in errors))

    def test_templates_form_valid_plan(self):
        assets = Path(__file__).resolve().parent.parent / 'assets'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'tasks').mkdir()
            for name in ('project', 'tasks'):
                (root / (name.upper() + '.md')).write_text(
                    (assets / (name + '.template.md')).read_text())
            (root / 'tasks' / 'CORE-01.md').write_text(
                (assets / 'task.template.md').read_text())
            self.assertEqual(validate(root), [])

    def test_cycle(self):
        self.task('A', 'B')
        self.register(a_deps='B')
        self.assertTrue(any('cycle' in e for e in validate(self.root)))

    def test_status_mismatch(self):
        self.task('A', 'none', 'done')
        self.assertTrue(any('mismatch' in e for e in validate(self.root)))

    def test_missing_dependency(self):
        self.task('A', 'MISSING')
        self.register(a_deps='MISSING')
        self.assertTrue(any('missing dependency' in e for e in validate(self.root)))

    def test_duplicate_id(self):
        (self.root / 'tasks' / 'duplicate.md').write_text('ID: A\nStatus: todo\nDependencies: none\n')
        self.assertTrue(any('duplicate task ID' in e for e in validate(self.root)))

    def test_hierarchy(self):
        sub = self.root / 'components' / 'one'
        (sub / 'tasks').mkdir(parents=True)
        (self.root / 'tasks' / 'B.md').rename(sub / 'tasks' / 'B.md')
        (sub / 'PROJECT.md').write_text('# Component\nSee task B in the root register.\n')
        p = self.root / 'TASKS.md'
        p.write_text(p.read_text().replace('tasks/B.md', 'components/one/tasks/B.md'))
        self.assertEqual(validate(self.root), [])

    def test_missing_guide(self):
        (self.root / 'PROJECT.md').unlink()
        self.assertEqual(validate(self.root), ['missing PROJECT.md'])

    def test_no_index_fallback(self):
        (self.root / 'TASKS.md').rename(self.root / 'INDEX.md')
        self.assertEqual(validate(self.root), ['missing TASKS.md'])

    def test_empty_register(self):
        (self.root / 'TASKS.md').write_text('# Tasks\n')
        self.assertIn('TASKS.md: missing task table', validate(self.root))

    def test_duplicate_register_row(self):
        p = self.root / 'TASKS.md'
        p.write_text(p.read_text() + '| A | Again | todo | none | [A](tasks/A.md) |\n')
        self.assertIn('TASKS.md: duplicate register row A', validate(self.root))

    def test_second_table(self):
        p = self.root / 'TASKS.md'
        p.write_text(p.read_text() + '\n' + p.read_text())
        self.assertIn('TASKS.md: expected one task table', validate(self.root))

    def test_unknown_task(self):
        p = self.root / 'TASKS.md'
        p.write_text(p.read_text() + '| C | Missing | todo | none | [C](tasks/C.md) |\n')
        self.assertIn('TASKS.md: unknown task C', validate(self.root))

    def test_wrong_task_link(self):
        p = self.root / 'TASKS.md'
        p.write_text(p.read_text().replace('tasks/A.md', 'tasks/B.md'))
        self.assertIn('TASKS.md: path/status/dependencies mismatch for A', validate(self.root))

    def test_missing_register_row(self):
        self.task('C', 'none')
        self.assertIn('task register missing C', validate(self.root))

    def test_cancelled_dependency(self):
        self.task('A', 'none', 'cancelled')
        self.register(a_status='cancelled')
        self.assertTrue(any('cancelled dependency' in e for e in validate(self.root)))

    def test_escaping_link(self):
        p = self.root / 'TASKS.md'
        p.write_text(p.read_text().replace('tasks/A.md', '../A.md'))
        self.assertTrue(any('escapes' in e for e in validate(self.root)))

    def test_markdown_links_to_paths_with_spaces(self):
        (self.root / 'tasks' / 'A.md').rename(self.root / 'tasks' / 'A one.md')
        path = self.root / 'TASKS.md'
        original = path.read_text()
        for destination in ('tasks/A%20one.md', '<tasks/A one.md>'):
            with self.subTest(destination=destination):
                path.write_text(original.replace('tasks/A.md', destination))
                self.assertEqual(validate(self.root), [])

    def test_percent_encoded_escaping_links_are_rejected(self):
        path = self.root / 'TASKS.md'
        original = path.read_text()
        for destination in ('%2e%2e/A.md', 'tasks/%2E%2E/%2E%2E/A.md'):
            with self.subTest(destination=destination):
                path.write_text(original.replace('tasks/A.md', destination))
                self.assertTrue(any('escapes' in error for error in validate(self.root)))

    def test_no_writes(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*.md')}
        validate(self.root)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*.md')}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
