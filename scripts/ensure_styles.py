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
HEADER_SNIPPET = '<header class="site-header">saylor allen</header>'


def process_file(path: Path, apply: bool) -> bool:
    text = path.read_text(encoding='utf-8')
    changed = False

    # ensure stylesheet link in head
    if 'href="styles.css"' not in text and "href='styles.css'" not in text:
        head_close = text.lower().find('</head>')
        if head_close == -1:
            print(f'SKIP (no </head>): {path}')
            return False
        text = text[:head_close] + LINK_TAG + '\n' + text[head_close:]
        changed = True

    # ensure site header exists in body
    if 'class="site-header"' not in text and "class='site-header'" not in text:
        body_open = text.lower().find('<body')
        if body_open != -1:
            body_start = text.find('>', body_open)
            if body_start != -1:
                insert_at = body_start + 1
                text = text[:insert_at] + '\n' + HEADER_SNIPPET + '\n' + text[insert_at:]
                changed = True

    if not changed:
        return False

    if apply:
        path.write_text(text, encoding='utf-8')
        print(f'Updated: {path}')
    else:
        print(f'Would update: {path}')
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
