#!/usr/bin/env python3
"""Validate the PROJECT.md/TASKS.md plan format; read-only, Python 3.9+ stdlib."""
import argparse
import re
from pathlib import Path
from urllib.parse import unquote

STATUSES = {'todo', 'in_progress', 'done', 'blocked', 'cancelled'}
ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]*$')
HEADER = ['ID', 'Task', 'Status', 'Dependencies', 'File']


def dependencies(value):
    if value.strip().lower() in ('none', '-', '—', ''):
        return []
    return [x.strip() for x in value.split(',')]


def field(text, name):
    matches = re.findall(r'^' + name + r':[ \t]*(.*?)[ \t]*$', text, re.M)
    if len(matches) != 1:
        raise ValueError('expected one ' + name + ' field')
    return matches[0]


def without_code_fences(text):
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^[ ]{0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if (match and match[1][0] == fence[0] and len(match[1]) >= fence[1]
                    and not match[2].strip()):
                fence = None
            continue
        if match:
            fence = (match[1][0], len(match[1]))
            lines.append('')  # A code block separates surrounding Markdown blocks.
        else:
            lines.append(line)
    return '\n'.join(lines)


def table_cells(line):
    text = line.strip()
    cells, start, backslashes = [], 1, 0
    for index, character in enumerate(text[1:], 1):
        if character == '|' and backslashes % 2 == 0:
            cells.append(text[start:index].strip())
            start = index + 1
        backslashes = backslashes + 1 if character == '\\' else 0
    if start < len(text):
        cells.append(text[start:].strip())
    return cells


def validate(directory):
    root = Path(directory).resolve()
    errors, tasks, rows = [], {}, {}
    guide = root / 'PROJECT.md'
    register = root / 'TASKS.md'
    for path in (guide, register):
        if not path.is_file():
            errors.append('missing ' + path.name)
    if errors:
        return errors
    # Task files live under tasks/ anywhere beneath the plan root.
    for path in sorted(root.rglob('*.md')):
        if 'tasks' not in path.relative_to(root).parts[:-1]:
            continue
        try:
            text = without_code_fences(path.read_text(encoding='utf-8'))
            ident, status = field(text, 'ID'), field(text, 'Status')
            deps = dependencies(field(text, 'Dependencies'))
            if not ID_RE.fullmatch(ident):
                raise ValueError('invalid task ID')
            if status not in STATUSES:
                raise ValueError('unknown status ' + status)
            if len(deps) != len(set(deps)):
                raise ValueError('duplicate dependency')
            if ident in tasks:
                raise ValueError('duplicate task ID ' + ident)
            tasks[ident] = (path.resolve(), status, deps)
        except (ValueError, OSError) as exc:
            errors.append(str(path.relative_to(root)) + ': ' + str(exc))
    active, found_table = False, False
    try:
        lines = iter(without_code_fences(register.read_text(encoding='utf-8')).splitlines())
        for line in lines:
            if not line.startswith('|'):
                active = False
                continue
            cells = table_cells(line)
            if cells == HEADER:
                if found_table:
                    raise ValueError('expected one task table')
                separator = next(lines, '')
                separator_cells = table_cells(separator) if separator.startswith('|') else []
                if (len(separator_cells) != len(HEADER)
                        or not all(re.fullmatch(r':?-+:?', cell) for cell in separator_cells)):
                    raise ValueError('missing or invalid task table separator')
                active = found_table = True
                continue
            if not active or all(re.fullmatch(r':?-+:?', c or ' ') for c in cells):
                continue
            if len(cells) != 5:
                raise ValueError('invalid task table row')
            ident, _, status, dep_text, link = cells
            if ident in rows:
                raise ValueError('duplicate register row ' + ident)
            match = re.fullmatch(r'\[[^\]]+\]\(([^)]+)\)', link)
            if not match:
                raise ValueError('invalid task link for ' + ident)
            destination = match[1]
            if destination.startswith('<') and destination.endswith('>'):
                destination = destination[1:-1]
            target = (register.parent / unquote(destination)).resolve()
            if not target.is_relative_to(root):
                raise ValueError('task link escapes plan directory: ' + ident)
            rows[ident] = (target, status, dependencies(dep_text))
        if not found_table:
            raise ValueError('missing task table')
    except (ValueError, OSError) as exc:
        errors.append('TASKS.md: ' + str(exc))
    if not tasks:
        errors.append('no task files found')
    for ident, row in rows.items():
        if ident not in tasks:
            errors.append('TASKS.md: unknown task ' + ident)
        elif row != tasks[ident]:
            errors.append('TASKS.md: path/status/dependencies mismatch for ' + ident)
    for ident, (_, _, deps) in tasks.items():
        if ident not in rows:
            errors.append('task register missing ' + ident)
        for dep in deps:
            if dep not in tasks:
                errors.append(ident + ': missing dependency ' + dep)
            elif tasks[dep][1] == 'cancelled':
                errors.append(ident + ': cancelled dependency must be rewired: ' + dep)
    visited, active = set(), set()
    for ident in tasks:
        if ident in visited:
            continue
        stack = [(ident, iter(tasks[ident][2]))]
        active.add(ident)
        while stack:
            current, pending = stack[-1]
            dep = next(pending, None)
            if dep is None:
                stack.pop()
                active.remove(current)
                visited.add(current)
            elif dep in active:
                chain = [entry[0] for entry in stack] + [dep]
                errors.append('dependency cycle: ' + ' -> '.join(chain))
            elif dep in tasks and dep not in visited:
                active.add(dep)
                stack.append((dep, iter(tasks[dep][2])))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan_directory', type=Path)
    args = parser.parse_args()
    errors = validate(args.plan_directory)
    for error in errors:
        print('ERROR: ' + error)
    if errors:
        return 1
    print('PASS: task links, statuses, dependencies and register coverage are consistent; graph is acyclic.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
