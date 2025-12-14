#!/usr/bin/env python3
"""
Generate sitemap.xml for MkDocs Material site

This script walks through the docs directory and creates a sitemap.xml
file containing all pages that will be built. It can generate either a simple
format (just URLs) or a detailed format (with lastmod, changefreq, and priority).
"""

import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET
from xml.dom import minidom


def get_markdown_files(docs_dir: str, exclude_patterns: List[str] = None,
                      languages: List[str] = None) -> List[Tuple[str, str]]:
    """
    Recursively find all markdown files in the docs directory.

    Args:
        docs_dir: Path to the docs directory
        exclude_patterns: List of patterns to exclude (e.g., ['z_*.md'])
        languages: List of language codes for i18n (e.g., ['en', 'zh-CN'])

    Returns:
        List of tuples (html_path, language_code) for each page
    """
    if exclude_patterns is None:
        exclude_patterns = ['z_*.md']

    if languages is None:
        languages = ['en']

    pages = []
    docs_path = Path(docs_dir)

    # Find all markdown files
    for md_file in docs_path.rglob('*.md'):
        relative_path = md_file.relative_to(docs_path)
        relative_str = str(relative_path)

        # Check if file should be excluded
        should_exclude = False
        for pattern in exclude_patterns:
            # Simple pattern matching (supports wildcards via startswith/contains)
            pattern_clean = pattern.strip('/')
            if '*' in pattern_clean:
                # Handle patterns like 'z_*.md'
                pattern_prefix = pattern_clean.split('*')[0]
                if relative_str.startswith(pattern_prefix) or os.path.basename(relative_str).startswith(pattern_prefix):
                    should_exclude = True
                    break
            elif pattern_clean in relative_str:
                should_exclude = True
                break

        if should_exclude:
            continue

        # Determine language and convert to HTML path
        # Files like 'file.zh-CN.md' are for Chinese, 'file.md' is for default (English)
        file_stem = md_file.stem
        lang_code = 'en'  # default

        # Check for language suffix
        for lang in languages:
            if lang != 'en' and file_stem.endswith(f'.{lang}'):
                lang_code = lang
                # Remove language suffix from the filename for the path
                file_stem = file_stem[:-len(f'.{lang}')]
                break

        # Convert .md to .html
        html_path = str(relative_path.parent / f"{file_stem}.html")

        # Normalize path separators for cross-platform compatibility
        html_path = html_path.replace('\\', '/')

        # For non-default languages, the path is prefixed with the language code
        if lang_code != 'en':
            html_path = f"{lang_code}/{html_path}"

        pages.append((html_path, lang_code))

    return sorted(pages)


def get_file_modification_time(docs_dir: str, md_path: str) -> str:
    """
    Get the last modification time of a markdown file in YYYY-MM-DD format.

    Args:
        docs_dir: Path to the docs directory
        md_path: Relative path to the markdown file

    Returns:
        Date string in YYYY-MM-DD format
    """
    file_path = Path(docs_dir) / md_path
    if file_path.exists():
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    else:
        # If file doesn't exist, use current date
        return datetime.now().strftime('%Y-%m-%d')


def create_simple_sitemap(base_url: str, pages: List[Tuple[str, str]]) -> ET.Element:
    """
    Create a simple sitemap with just URLs (similar to the reference sitemap).

    Args:
        base_url: Base URL of the site (e.g., 'https://pokemonautomation.github.io')
        pages: List of tuples (html_path, language_code)

    Returns:
        XML Element representing the sitemap
    """
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    for html_path, lang_code in pages:
        url_elem = ET.SubElement(urlset, 'url')

        loc = ET.SubElement(url_elem, 'loc')
        loc.text = f"{base_url.rstrip('/')}/{html_path}"

    return urlset


def md_path_from_html(html_path: str, lang_code: str) -> str:
    """
    Convert HTML path back to markdown path.

    Args:
        html_path: Path to HTML file (e.g., 'Developer/index.html' or 'zh-CN/Developer/index.html')
        lang_code: Language code

    Returns:
        Relative path to the markdown file in docs directory
    """
    # Remove language prefix if present
    if lang_code != 'en' and html_path.startswith(f'{lang_code}/'):
        html_path = html_path[len(f'{lang_code}/'):]

    # Convert .html to .md
    md_path = html_path.replace('.html', '.md')

    # Add language suffix for non-English
    if lang_code != 'en':
        md_path = md_path.replace('.md', f'.{lang_code}.md')

    return md_path


def create_detailed_sitemap(base_url: str, pages: List[Tuple[str, str]], docs_dir: str,
                          changefreq: str = 'daily', priority: str = None) -> ET.Element:
    """
    Create a detailed sitemap with lastmod, changefreq, and optionally priority.

    Args:
        base_url: Base URL of the site
        pages: List of tuples (html_path, language_code)
        docs_dir: Path to the docs directory (for getting modification times)
        changefreq: Change frequency value (always, hourly, daily, weekly, monthly, yearly, never)
        priority: Priority value (0.0 to 1.0) or None to omit

    Returns:
        XML Element representing the sitemap
    """
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    for html_path, lang_code in pages:
        url_elem = ET.SubElement(urlset, 'url')

        # Location
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = f"{base_url.rstrip('/')}/{html_path}"

        # Last modification date - get from source markdown file
        md_path = md_path_from_html(html_path, lang_code)
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = get_file_modification_time(docs_dir, md_path)

        # Change frequency
        if changefreq:
            changefreq_elem = ET.SubElement(url_elem, 'changefreq')
            changefreq_elem.text = changefreq

        # Priority (optional)
        if priority:
            priority_elem = ET.SubElement(url_elem, 'priority')
            priority_elem.text = str(priority)

    return urlset


def prettify_xml(elem: ET.Element) -> str:
    """
    Return a pretty-printed XML string for the Element.

    Args:
        elem: XML Element to prettify

    Returns:
        Pretty-printed XML string
    """
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='    ', encoding='UTF-8').decode('utf-8')


def main():
    parser = argparse.ArgumentParser(
        description='Generate sitemap.xml for MkDocs Material site',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate simple sitemap (URLs only)
  python generate_sitemap.py

  # Generate detailed sitemap with lastmod and changefreq
  python generate_sitemap.py --detailed

  # Generate sitemap with custom base URL
  python generate_sitemap.py --base-url https://example.com

  # Generate sitemap with custom change frequency and priority
  python generate_sitemap.py --detailed --changefreq weekly --priority 0.8

  # Specify custom docs directory and output file
  python generate_sitemap.py --docs-dir ./docs --output ./custom-sitemap.xml

  # Include multiple languages
  python generate_sitemap.py --languages en zh-CN ja
        """
    )

    parser.add_argument(
        '--docs-dir',
        default='docs',
        help='Path to the docs directory (default: docs)'
    )

    parser.add_argument(
        '--output',
        default='sitemap.xml',
        help='Output sitemap file path (default: sitemap.xml)'
    )

    parser.add_argument(
        '--base-url',
        default='https://pokemonautomation.github.io',
        help='Base URL of the site (default: https://pokemonautomation.github.io)'
    )

    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Generate detailed sitemap with lastmod and changefreq'
    )

    parser.add_argument(
        '--changefreq',
        choices=['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never'],
        default='daily',
        help='Change frequency (default: daily, only used with --detailed)'
    )

    parser.add_argument(
        '--priority',
        type=float,
        help='Priority value 0.0-1.0 (optional, only used with --detailed)'
    )

    parser.add_argument(
        '--exclude',
        nargs='*',
        default=['z_*.md'],
        help='Patterns to exclude from sitemap (default: z_*.md)'
    )

    parser.add_argument(
        '--languages',
        nargs='*',
        default=['en', 'zh-CN'],
        help='Language codes for i18n (default: en zh-CN)'
    )

    args = parser.parse_args()

    # Check if docs directory exists
    if not os.path.isdir(args.docs_dir):
        print(f"Error: Docs directory '{args.docs_dir}' does not exist.")
        print("Please specify correct --docs-dir")
        return 1

    # Get all markdown files and convert to pages
    print(f"Scanning for markdown files in '{args.docs_dir}'...")
    pages = get_markdown_files(args.docs_dir, args.exclude, args.languages)
    print(f"Found {len(pages)} pages")

    if len(pages) == 0:
        print("Warning: No pages found. Check your --docs-dir and --exclude settings.")
        return 1

    # Create sitemap
    print(f"Generating {'detailed' if args.detailed else 'simple'} sitemap...")
    if args.detailed:
        urlset = create_detailed_sitemap(
            args.base_url,
            pages,
            args.docs_dir,
            args.changefreq,
            args.priority
        )
    else:
        urlset = create_simple_sitemap(args.base_url, pages)

    # Write to file
    xml_string = prettify_xml(urlset)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(xml_string)

    print(f"Sitemap generated successfully: {args.output}")
    print(f"Total URLs: {len(pages)}")

    # Show language breakdown
    lang_counts = {}
    for _, lang_code in pages:
        lang_counts[lang_code] = lang_counts.get(lang_code, 0) + 1

    for lang, count in sorted(lang_counts.items()):
        print(f"  - {lang}: {count} pages")

    return 0


if __name__ == '__main__':
    exit(main())
