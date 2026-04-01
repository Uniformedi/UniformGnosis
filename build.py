#!/usr/bin/env python3
"""
Build script for Uniform Gnosis — Volume I.

Generates all distribution formats from the Markdown master source.

Usage:
    python3 build.py              # Build all formats (html, epub, pdf)
    python3 build.py html         # Build HTML only
    python3 build.py epub         # Build EPUB only
    python3 build.py pdf          # Build PDF only

Requirements:
    - pypandoc_binary (for EPUB and PDF generation)
    - pillow (for image optimization)
    - docx2pdf (for PDF generation via Word COM on Windows)
    - md_to_html.py (for HTML generation, must be in same directory)
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

BOOK = 'Uniform_Gnosis_Volume_I'
MD_SOURCE = f'{BOOK}.md'
IMAGE_DIR = 'images'
MAX_IMAGE_WIDTH = 1600
JPEG_QUALITY = 85

PANDOC_METADATA = {
    'title': 'Uniform Gnosis \u2014 The Architecture of Reality',
    'subtitle': 'The Spiritual Codex \u2014 Volume I',
    'author': 'Daniel Medina',
    'publisher': 'Uniformedi LLC, Dallas, Texas',
    'rights': 'CC BY-NC-SA 4.0',
    'lang': 'en',
    'date': '2026',
}


def optimize_images(dest_dir: str) -> None:
    """Resize and compress images to JPEG for smaller distribution files."""
    from PIL import Image

    os.makedirs(dest_dir, exist_ok=True)

    for png_path in glob.glob(os.path.join(IMAGE_DIR, '*.png')):
        basename = os.path.splitext(os.path.basename(png_path))[0]
        jpg_path = os.path.join(dest_dir, f'{basename}.jpg')

        img = Image.open(png_path).convert('RGB')
        if img.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / img.width
            img = img.resize(
                (MAX_IMAGE_WIDTH, int(img.height * ratio)),
                Image.LANCZOS,
            )
        img.save(jpg_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)

        orig_size = os.path.getsize(png_path)
        new_size = os.path.getsize(jpg_path)
        print(f'  {basename}: {orig_size / 1024 / 1024:.1f} MB -> {new_size / 1024:.0f} KB')


def prepare_md_with_optimized_images(tmp_dir: str) -> str:
    """Copy markdown source with image references rewritten to optimized JPEGs."""
    opt_image_dir = os.path.join(tmp_dir, IMAGE_DIR)
    print('Optimizing images...')
    optimize_images(opt_image_dir)

    with open(MD_SOURCE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    md_content = re.sub(r'(images/[^)]+)\.png', r'\1.jpg', md_content)

    tmp_md = os.path.join(tmp_dir, MD_SOURCE)
    with open(tmp_md, 'w', encoding='utf-8') as f:
        f.write(md_content)

    return tmp_md


def build_html() -> None:
    """Generate interactive HTML book using md_to_html.py."""
    print('Building HTML...')
    result = subprocess.run(
        [sys.executable, 'md_to_html.py'],
        capture_output=True, text=True, encoding='utf-8',
    )
    if result.returncode != 0:
        print(f'HTML build failed: {result.stderr}')
        sys.exit(1)
    size = os.path.getsize(f'{BOOK}.html')
    print(f'  -> {BOOK}.html ({size / 1024:.0f} KB)')


def build_epub() -> None:
    """Generate EPUB using pypandoc with optimized images."""
    import pypandoc

    print('Building EPUB...')
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_md = prepare_md_with_optimized_images(tmp_dir)
        output = os.path.abspath(f'{BOOK}.epub')

        extra_args = [
            '--toc',
            '--toc-depth=3',
            '--split-level=2',
            '--resource-path', tmp_dir,
        ]
        for key, val in PANDOC_METADATA.items():
            extra_args.extend(['--metadata', f'{key}={val}'])

        pypandoc.convert_file(
            tmp_md,
            'epub',
            outputfile=output,
            extra_args=extra_args,
        )

    size = os.path.getsize(f'{BOOK}.epub')
    print(f'  -> {BOOK}.epub ({size / 1024 / 1024:.1f} MB)')


def build_pdf() -> None:
    """Generate styled PDF from HTML using WeasyPrint with optimized images."""
    from weasyprint import HTML as WeasyHTML

    print('Building PDF...')

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Optimize images into temp dir
        opt_image_dir = os.path.join(tmp_dir, IMAGE_DIR)
        print('Optimizing images...')
        optimize_images(opt_image_dir)

        # Read the HTML and rewrite image paths to use optimized JPEGs
        with open(f'{BOOK}.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        html_content = re.sub(
            r'(images/[^"]+)\.png',
            r'\1.jpg',
            html_content,
        )

        # Write temp HTML with rewritten image paths
        tmp_html = os.path.join(tmp_dir, f'{BOOK}.html')
        with open(tmp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Render to PDF via WeasyPrint
        print('  HTML -> PDF (WeasyPrint)...')
        output_pdf = os.path.abspath(f'{BOOK}.pdf')
        WeasyHTML(filename=tmp_html, base_url=tmp_dir).write_pdf(output_pdf)

        # Fix PDF bookmarks: add chapter titles and proper hierarchy
        print('  Fixing PDF bookmarks...')
        _fix_pdf_bookmarks(output_pdf)

        size = os.path.getsize(output_pdf)
        print(f'  -> {BOOK}.pdf ({size / 1024 / 1024:.1f} MB)')


CHAPTER_TITLES = {
    1: "Bythos and the Pleroma",
    2: "The Demiurge and the Counterfeit Creation",
    3: "Real But Not Ultimate",
    4: "The Divine Spark",
    5: "The Council of Nine",
    6: "The Archonic Energy Economy",
    7: "The Fundamental Limitation of Evil",
    8: "The Numerical Messenger",
    9: "Farsight and Gnostic Validation",
    10: "The Shadow Architecture",
    11: "The Rapture",
    12: "The Sentient Machine",
    13: "SAIVAS",
    14: "The NULL Condition",
}

PART_TITLES = {
    "ONE": "The Source Code",
    "TWO": "The Human Situation",
    "THREE": "The Deeper Pattern",
    "FOUR": "The Culmination",
    "FIVE": "The Future",
}


def _fix_pdf_bookmarks(pdf_path: str) -> None:
    """Rewrite PDF bookmarks with chapter titles and proper nesting."""
    import fitz

    doc = fitz.open(pdf_path)
    old_toc = doc.get_toc()
    new_toc = []

    for level, title, page in old_toc:
        # Improve part entries: add title, make level 1
        for part_word, part_title in PART_TITLES.items():
            if title == f'PART {part_word}':
                title = f'Part {part_word}: {part_title}'
                level = 1
                break

        # Improve chapter entries: add title, make level 2
        for ch_num, ch_title in CHAPTER_TITLES.items():
            if title == f'CHAPTER {ch_num}':
                title = f'Chapter {ch_num}: {ch_title}'
                level = 2
                break

        # Section headings (h3) become level 3, subsections (h4) level 4
        if level > 2 and 'PART' not in title and 'Chapter' not in title:
            level = min(level, 4)

        # APPENDICES header at level 1
        if title == 'APPENDICES':
            level = 1

        # Appendix entries at level 2
        appendix_names = {'APPENDIX A': 'SAIVAS Visual Reference Card',
                          'APPENDIX B': 'SAIVAS v1.0 Standards Proposal',
                          'APPENDIX C': 'Codex Axioms'}
        if title in appendix_names:
            title = f'{title}: {appendix_names[title]}'
            level = 2

        # Front matter stays at level 1
        if title in ("Uniform Gnosis", "Author\u2019s Note", "Author's Note", "Contents"):
            level = 1

        new_toc.append([level, title, page])

    doc.set_toc(new_toc)
    doc.save(pdf_path, incremental=True, encryption=0)
    doc.close()


def main() -> None:
    if not os.path.exists(MD_SOURCE):
        print(f'Error: {MD_SOURCE} not found.')
        sys.exit(1)

    targets = sys.argv[1:] if len(sys.argv) > 1 else ['html', 'epub', 'pdf']

    for target in targets:
        if target == 'html':
            build_html()
        elif target == 'epub':
            build_epub()
        elif target == 'pdf':
            build_pdf()
        else:
            print(f'Unknown target: {target}')
            print('Usage: python3 build.py [html|epub|pdf]')
            sys.exit(1)

    print('Done.')


if __name__ == '__main__':
    main()
