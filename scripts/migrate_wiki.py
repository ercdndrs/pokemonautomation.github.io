#!/usr/bin/env python3
"""
Script to migrate old wiki files to point to the new GitHub Pages site.

Usage:
    python migrate_wiki.py                  # Dry-run mode: show correspondences
    python migrate_wiki.py --apply          # Apply edits to old wiki files
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Base directories
OLD_WIKI_DIR = Path("../ComputerControl/Wiki")
NEW_WIKI_DIR = Path("docs")
GITHUB_PAGES_BASE_URL = "https://pokemonautomation.github.io"


def normalize_path(path: Path, base: Path) -> str:
    """Get relative path from base directory."""
    return str(path.relative_to(base))


def get_new_path(old_path: Path) -> Optional[Path]:
    """
    Map an old wiki path to the new GitHub Pages path.

    Mapping rules:
    - README.md -> index.md
    - Wiki/ prefix is removed (maps to docs/)
    - Software/Discord* -> DiscordIntegration/*
    - Everything else stays the same
    """
    # Get relative path from old wiki directory
    rel_path = old_path.relative_to(OLD_WIKI_DIR)

    # Convert path parts
    parts = list(rel_path.parts)

    # Special case: Software/Discord* -> DiscordIntegration/*
    if len(parts) >= 2 and parts[0] == "Software" and parts[1].startswith("Discord"):
        parts[0] = "DiscordIntegration"
        # Special case: DiscordIntegration.md -> index.md
        if parts[1] == "DiscordIntegration.md":
            parts[1] = "index.md"

    # Handle README.md -> index.md conversion
    if parts[-1] == "README.md":
        parts[-1] = "index.md"

    # Construct new path
    new_path = NEW_WIKI_DIR / Path(*parts)

    return new_path


def get_github_pages_url(old_path: Path) -> str:
    """
    Get the GitHub Pages URL for an old wiki file.

    Converts:
    - .md extension to .html
    - Maps path to new location
    """
    new_path = get_new_path(old_path)

    # Get relative path from docs directory
    rel_path = new_path.relative_to(NEW_WIKI_DIR)

    # Convert to URL path (change .md to .html)
    url_path = str(rel_path).replace(".md", ".html")

    # Construct full URL
    return f"{GITHUB_PAGES_BASE_URL}/{url_path}"


def create_redirect_content(title: str, url: str) -> str:
    """
    Create the redirect content for an old wiki file.
    Uses the pattern from the manually renamed files.
    """
    return f"""# {title}

This page has moved here: {url}

"""


def extract_title_from_file(file_path: Path) -> str:
    """
    Extract the title from a markdown file.
    Assumes the first line starting with # is the title.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass

    # Fallback: use filename without extension
    return file_path.stem.replace("-", " ").replace("_", " ")


def find_all_markdown_files(directory: Path) -> List[Path]:
    """Find all markdown files in a directory recursively."""
    return sorted(directory.glob("**/*.md"))


def main():
    parser = argparse.ArgumentParser(
        description="Migrate old wiki files to point to new GitHub Pages site"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply edits to old wiki files (default is dry-run)"
    )

    args = parser.parse_args()

    # Check if old wiki directory exists
    if not OLD_WIKI_DIR.exists():
        print(f"Error: Old wiki directory not found: {OLD_WIKI_DIR}")
        sys.exit(1)

    # Check if new wiki directory exists
    if not NEW_WIKI_DIR.exists():
        print(f"Error: New wiki directory not found: {NEW_WIKI_DIR}")
        sys.exit(1)

    # Find all markdown files in old wiki
    old_files = find_all_markdown_files(OLD_WIKI_DIR)

    print(f"Found {len(old_files)} markdown files in old wiki")
    print(f"Mode: {'APPLY EDITS' if args.apply else 'DRY-RUN'}")
    print("=" * 80)
    print()

    # Track statistics
    matched = []
    not_matched = []
    already_redirected = []

    for old_file in old_files:
        rel_old = old_file.relative_to(OLD_WIKI_DIR)
        new_file = get_new_path(old_file)

        # Check if new file exists
        if new_file.exists():
            # Check if old file is already a redirect
            with open(old_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "This page has moved here:" in content:
                    already_redirected.append((old_file, new_file))
                else:
                    matched.append((old_file, new_file))
        else:
            not_matched.append((old_file, new_file))

    # Print matched files
    if matched:
        print(f"MATCHED ({len(matched)} files):")
        print("-" * 80)
        for old_file, new_file in matched:
            rel_old = old_file.relative_to(OLD_WIKI_DIR)
            rel_new = new_file.relative_to(NEW_WIKI_DIR)
            url = get_github_pages_url(old_file)
            print(f"  {rel_old}")
            print(f"    -> {rel_new}")
            print(f"    -> {url}")
            print()
        print()

    # Print already redirected files
    if already_redirected:
        print(f"ALREADY REDIRECTED ({len(already_redirected)} files):")
        print("-" * 80)
        for old_file, new_file in already_redirected:
            rel_old = old_file.relative_to(OLD_WIKI_DIR)
            print(f"  {rel_old} (already redirected)")
        print()

    # Print non-matched files
    if not_matched:
        print(f"NO MATCH ({len(not_matched)} files):")
        print("-" * 80)
        for old_file, new_file in not_matched:
            rel_old = old_file.relative_to(OLD_WIKI_DIR)
            rel_new = new_file.relative_to(NEW_WIKI_DIR)
            print(f"  {rel_old}")
            print(f"    -> {rel_new} (NOT FOUND)")
        print()

    # Apply edits if requested
    if args.apply:
        print("=" * 80)
        print("APPLYING EDITS...")
        print("=" * 80)
        print()

        for old_file, new_file in matched:
            rel_old = old_file.relative_to(OLD_WIKI_DIR)

            # Extract title from original file
            title = extract_title_from_file(old_file)

            # Get GitHub Pages URL
            url = get_github_pages_url(old_file)

            # Create redirect content
            redirect_content = create_redirect_content(title, url)

            # Write to old file
            with open(old_file, 'w', encoding='utf-8') as f:
                f.write(redirect_content)

            print(f"✓ Updated: {rel_old}")

        print()
        print(f"Successfully updated {len(matched)} files!")
    else:
        print("=" * 80)
        print("DRY-RUN MODE: No files were modified.")
        print("Run with --apply to apply edits.")
        print("=" * 80)

    # Print summary
    print()
    print("SUMMARY:")
    print(f"  Total files: {len(old_files)}")
    print(f"  Matched: {len(matched)}")
    print(f"  Already redirected: {len(already_redirected)}")
    print(f"  No match: {len(not_matched)}")


if __name__ == "__main__":
    main()
