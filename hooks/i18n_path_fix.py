"""
MkDocs hook to fix image src paths for multi-language sites.

PROBLEM:
--------
When using mkdocs-static-i18n, translated pages are served under /<lang>/ subdirectory:
  - English: /ControllerList.html
  - Simplified Chinese: /zh-CN/ControllerList.html

But image paths used in the pages are still the same (e.g., /SetupGuide/Images/foo.jpg).
So relative image paths break in translated pages:
  - From /ControllerList.html: "SetupGuide/Images/foo.jpg" → /SetupGuide/Images/foo.jpg ✓
  - From /zh-CN/ControllerList.html: "SetupGuide/Images/foo.jpg" → /zh-CN/SetupGuide/Images/foo.jpg ✗

SOLUTION:
---------
Convert relative path to go to the root, then add extra '../' to escape the /<lang>/ directory.

KEY INSIGHT:
------------
We process ALL pages (English + Simplified Chinese) with the SAME path transformations.
The transformed paths work for BOTH languages because:
  1. Simplified Chinese needs extra '../' to escape /zh-CN/
  2. English works with extra '../' too (can't go above root, so harmless)

EXAMPLE 1 - Root level page (ControllerList.md):
  Image path in the page: "SetupGuide/Images/foo.jpg"
  Transformed path:       "../SetupGuide/Images/foo.jpg"

  English webpage: /ControllerList.html:
    "../" goes to "/" (root) → /SetupGuide/Images/foo.jpg ✓

  Simplified Chinese webpage: /zh-CN/ControllerList.html:
    "../" goes to "/" (escapes /zh-CN/) → /SetupGuide/Images/foo.jpg ✓

EXAMPLE 2 - Nested page (SetupGuide/Controllers/Controller-ESP32-S3.md):
  Image path in the page: "../Images/foo.jpg" (up one level: Controllers → SetupGuide → Images)
  Transformed path:       "../../../SetupGuide/Images/foo.jpg" (up to root, then down to target)

  English /SetupGuide/Controllers/Controller-ESP32-S3.html:
    "../../../" tries to go up 3 levels but stops at "/" (root)
    → /SetupGuide/Images/foo.jpg ✓

  Simplified Chinese /zh-CN/SetupGuide/Controllers/Controller-ESP32-S3.html:
    "../../../" goes up 3 levels: Controllers → SetupGuide → zh-CN → root "/"
    → /SetupGuide/Images/foo.jpg ✓

WHEN IT RUNS:
-------------
The i18n plugin builds the site multiple times (once per language):
  1. English build: Hook processes all pages, adds extra '../' at root level (still works for English)
  2. Simplified Chinese build: Hook processes all pages, adds extra '../' at root level to escape /zh-CN/
  3. Fallback pages (English pages when there is no translations) are copied to /zh-CN/ with fixed paths
"""

import re
import logging

log = logging.getLogger('mkdocs.plugins.i18n_path_fix')

# List of language codes used in the site (add more as needed, e.g., ['zh-CN', 'zh-TW'])
LANGUAGES = ['zh-CN']


def on_page_markdown(markdown: str, page, config, files) -> str:
    """
    Fix relative paths in markdown files to work in both default and translated language builds.

    This hook is called by MkDocs for every page during the build process.
    It modifies image src attributes to add extra '../' levels to fix language-specific URL paths
    like /zh-CN/.

    Args:
        markdown: The markdown content of the page
        page: MkDocs page object with metadata
        config: MkDocs configuration
        files: Collection of all site files

    Returns:
        Modified markdown with fixed paths
    """
    # Extract the directory path of the source file, e.g. get "SetupGuide/Controllers" from
    # "SetupGuide/Controllers/Controller-ESP32-S3.md"
    # This tells us how deeply nested the page is in the directory structure
    src_dir = page.file.src_uri.rsplit('/', 1)[0] if '/' in page.file.src_uri else ''
    # Parse the source directory structure
    # e.g., "SetupGuide/Controllers/" → ["SetupGuide", "Controllers"]
    src_parts = src_dir.split('/') if src_dir else []

    # Fix all image paths in a single pass
    markdown = _fix_image_paths(markdown, src_parts)

    # Note: We do NOT modify markdown links ([text](page.md))
    # MkDocs expects links to stay as .md and converts them to .html automatically
    # The i18n plugin handles keeping links within the correct language directory

    return markdown


def _fix_image_paths(markdown: str, src_parts: list[str]) -> str:
    """
    Fix all image src paths to work correctly with multi-language sites.

    This function handles four types of image paths:
    1. External links (http://, https://) → No changes
    2. Absolute paths starting with '/' → Add '../' to escape language directory
    3. Relative paths  → add "../" to to to root, add one more "../" to escape language directory,
       then back to the target file

    Examples:
        Source file: Programs/PokemonBDSP/EggFetcher.md (depth=2)

        Type 1: external link:
            "https://example.com/image.png" → no change

        Type 2: absolute path:
            "/SetupGuide/Images/foo.jpg" → no change

        Type 3 relative path:
            "../images/foo.jpg" → "../../../Programs/images/foo.jpg"
            use "../.." to go back to root, add another "../" to escape the language directory, then
            "Programs/images/foo.jpg" to reach the target file.

    Args:
        markdown: The markdown content
        src_parts: Directory components of source file (e.g., ["Programs", "PokemonBDSP"])
        src_dir: Source directory string (e.g., "Programs/PokemonBDSP")

    Returns:
        Markdown with all image paths fixed for multi-language support
    """
    def fix_path(match):
        original_path = match.group(1)

        # Type 1: External links: no change
        if original_path.startswith('http://') or original_path.startswith('https://'):
            return match.group(0)

        # Type 2: Absolute paths starting with '/': no change
        if original_path.startswith('/'):
            return match.group(0)

        # Type 3: Relative paths (starting with '../' or simple paths like "images/foo.png")
        
        # Count how many levels we go up in the original path
        up_count = 0
        path_remainder = original_path
        while path_remainder.startswith('../'):
            up_count += 1
            path_remainder = path_remainder[3:]  # Remove '../'

        # Calculate the parent directory after going up 'up_count' levels
        # e.g., from ["Programs", "PokemonBDSP"], going up 1 level → ["Programs"]
        parent_parts = src_parts[:-up_count] if up_count > 0 else src_parts

        # Build new path:
        # 1. Go up to root: '../' x (depth + 1) for language support
        # 2. Go back down to parent directory (if any)
        # 3. Append the remainder
        new_up_count = len(src_parts) + 1  # +1 to escape the language directory
        new_path = '../' * new_up_count

        if parent_parts:
            new_path += '/'.join(parent_parts) + '/'

        new_path += path_remainder
        return f'src="{new_path}"'

    # Find all image src attributes and fix them
    # Regex: src="([^"]+)" matches all src="anything"
    return re.sub(r'src="([^"]+)"', fix_path, markdown)
