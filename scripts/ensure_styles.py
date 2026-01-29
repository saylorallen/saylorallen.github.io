#!/usr/bin/env python3
"""Scan HTML files and ensure a link to styles.css is present in the <head>.

Usage:
  python scripts/ensure_styles.py [--apply]

Without --apply the script prints what it would change (dry run).
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_TAG = '<link rel="stylesheet" href="styles.css">'


def process_file(path: Path, apply: bool) -> bool:
    text = path.read_text(encoding='utf-8')
    if 'href="styles.css"' in text or "href='styles.css'" in text:
        return False

    head_close = text.lower().find('</head>')
    if head_close == -1:
        # can't reliably insert, skip
        print(f'SKIP (no </head>): {path}')
        return False

    insert_at = head_close
    new_text = text[:insert_at] + LINK_TAG + '\n' + text[insert_at:]

    if apply:
        path.write_text(new_text, encoding='utf-8')
        print(f'Updated: {path}')
    else:
        print(f'Would add link to: {path}')
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--apply', action='store_true', help='Write changes instead of dry-run')
    args = p.parse_args()

    changed = 0
    for path in ROOT.rglob('*.html'):
        # skip files in .git or in scripts folder
        if '.git' in path.parts or 'scripts' in path.parts:
            continue
        if process_file(path, args.apply):
            changed += 1

    if changed == 0:
        print('No files needed changes.')


if __name__ == '__main__':
    main()
