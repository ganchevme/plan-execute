#!/usr/bin/env python3
"""Check a repository or full source archive; read-only, Python 3.9+ stdlib.

Git checkouts include tracked and unignored files, read from the working tree.
Archives include all files except Git metadata, virtual environments and caches.
This checks file references and release contents, not agent behavior or secrets.
"""
import fnmatch
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DEV_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}
REQUIRED = {
    'SKILL.md', 'README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', 'SECURITY.md',
    '.gitignore', '.github/workflows/validate.yml', 'scripts/check_package.py',
    'agents/openai.yaml', 'assets/settings.example.toml', 'assets/project.template.md',
    'assets/tasks.template.md', 'assets/task.template.md', 'references/planning.md',
    'references/execution.md', 'references/settings.md', 'references/large-projects.md',
    'references/logs-wrapper.md', 'scripts/validate_plan.py', 'scripts/test_validate_plan.py',
    'scripts/test_check_package.py',
}
FORBIDDEN = (
    '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '*.log', '*.tar', '*.tar.gz', '*.tgz',
    '*.zip', '*.exe', '*.dll', '*.so', '*.dylib', '*.pem', '*.key', '*.p12', '*.pfx',
    '*.local', '*.local.*',
)


def package_files(root):
    if (root / '.git').exists():
        result = subprocess.run(
            ['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
            check=True, stdout=subprocess.PIPE,
        )
        return {name.decode('utf-8') for name in result.stdout.split(b'\0') if name}
    return {p.relative_to(root).as_posix() for p in root.rglob('*')
            if (p.is_symlink() or p.is_file())
            and not DEV_DIRS.intersection(p.relative_to(root).parts)}


def check(root):
    root = root.resolve()
    files = package_files(root)
    errors = ['missing package file: ' + name for name in sorted(REQUIRED - files)]
    texts = {}
    for name in sorted(files):
        path = root / name
        parts = Path(name).parts
        private_env = Path(name).name.startswith('.env') and not name.endswith(('.example', '.sample'))
        if (DEV_DIRS.intersection(parts) or parts[0] in {'versions', 'logs', 'build', 'dist'}
                or name.startswith('assets/logs-wrapper/') or name == 'plan/settings.toml'
                or private_env or any(fnmatch.fnmatch(Path(name).name, p) for p in FORBIDDEN)):
            errors.append('excluded release artifact: ' + name)
        if path.is_symlink() or not path.is_file():
            errors.append('missing file or unsupported symlink: ' + name)
            continue
        try:
            texts[name] = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append('non-text release file: ' + name)

    skill = texts.get('SKILL.md', '')
    frontmatter = re.match(r'\A---\n(.*?)\n---(?:\n|$)', skill, re.S)
    header = frontmatter.group(1) if frontmatter else ''
    if not re.search(r'^name: plan-execute\s*$', header, re.M):
        errors.append('SKILL.md: missing plan-execute name in frontmatter')
    if not re.search(r'^description: \S', header, re.M):
        errors.append('SKILL.md: missing description in frontmatter')
    version = re.search(r'^  version: [\"\']?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)[\"\']?\s*$', header, re.M)
    if not version:
        errors.append('SKILL.md: missing release version in metadata')
    elif not re.search(r'^##\s+\[?' + re.escape(version.group(1)) + r'\]?(?:\s|$)',
                       texts.get('CHANGELOG.md', ''), re.M):
        errors.append('CHANGELOG.md: missing entry for ' + version.group(1))

    for name, text in texts.items():
        if not name.endswith('.md') or name.startswith('assets/'):
            continue  # Templates contain links intended for generated project files.
        text = re.sub(r'(?ms)^```[^\n]*\n.*?^```\s*$', '', text)
        text = re.sub(r'`[^`\n]*`', '', text)
        for href in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text):
            link = urlsplit(href.strip('<>'))
            if link.scheme or link.netloc or not link.path:
                continue
            target = (root / name).parent / unquote(link.path)
            resolved = target.resolve()
            if not resolved.is_relative_to(root) or resolved.relative_to(root).as_posix() not in files:
                errors.append(name + ': missing packaged link target: ' + href)
    return errors, len(files)


if __name__ == '__main__':
    problems, count = check(ROOT)
    for problem in problems:
        print('ERROR: ' + problem)
    if not problems:
        print(f'PASS: {count} package files; required resources, release version and local file links are consistent.')
    raise SystemExit(bool(problems))
