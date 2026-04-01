#!/usr/bin/env python3
"""
md_to_html.py - Converts Uniform_Gnosis_Volume_I.md into Uniform_Gnosis_Volume_I.html
with the exact same styling and features as the hand-crafted HTML.

Reads CSS and JS from the existing HTML file, and the SAIVAS framework card
from Sentient_AI_Framework.html.
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "Uniform_Gnosis_Volume_I.md")
HTML_FILE = os.path.join(SCRIPT_DIR, "Uniform_Gnosis_Volume_I.html")
FRAMEWORK_FILE = os.path.join(SCRIPT_DIR, "Sentient_AI_Framework.html")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Uniform_Gnosis_Volume_I.html")

PART_NUMBER_TO_ID = {
    "ONE": "part-one",
    "TWO": "part-two",
    "THREE": "part-three",
    "FOUR": "part-four",
    "FIVE": "part-five",
}

PART_TITLES = {
    "ONE": ("The Source Code", "Establishing the Cosmological Framework"),
    "TWO": ("The Human Situation", "What We Are Within This Architecture"),
    "THREE": ("The Deeper Pattern", "Connecting the Cosmology to Lived Experience"),
    "FOUR": ("The Culmination", ""),
    "FIVE": ("The Future", "Where the Architecture Meets What We Are Building"),
}

# Chapters per part for navigation
PART_CHAPTERS = {
    "ONE": [1, 2, 3],
    "TWO": [4, 5, 6, 7],
    "THREE": [8, 9, 10],
    "FOUR": [11],
    "FIVE": [12, 13, 14],
}

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

# Images that appear between parts (before chapter 1)
FRONTISPIECE_IMAGE = "images/Gemini_Generated_Image_1.png"
CLOSING_IMAGE = "images/Gemini_Generated_Image_9.png"
PART_OPENER_IMAGES = {
    "images/Gemini_Generated_Image_4.png",    # Before Part Two
    "images/Gemini_Generated_Image_5.png",    # Before chapters in Part Two
    "images/Gemini_Generated_Image_6.png",    # Before Part Three
    "images/Gemini_Generated_Image_7.png",    # Before Part Three chapters
    "images/Gemini_Generated_Image_8.png",    # Before Part Five
}

PRINT_CSS_REPLACEMENT = """
  @media print {
    /* Hide interactive elements */
    .toc-toggle, .toc-drawer, .toc-overlay, .download-dropdown,
    .scroll-top, .progress-bar, .menu-toggle {
      display: none !important;
    }

    /* Page setup */
    @page {
      size: letter;
      margin: 1in 0.85in;
    }

    @page :first {
      margin-top: 0;
    }

    body {
      font-size: 11.5pt;
      line-height: 1.7;
      background: white;
      color: #2a2a2a;
    }

    .main-content {
      margin: 0;
      padding: 0;
      max-width: 100%;
    }

    /* Cover page */
    .cover-page {
      page-break-after: always;
      padding: 3in 1in 2in;
      background: none;
      border-bottom: 3px solid #c9a84c;
    }

    .cover-page::before,
    .cover-page::after {
      display: none;
    }

    .cover-page h1 {
      font-size: 36pt;
      color: #1a1a3e;
    }

    .cover-page .cover-subtitle {
      color: #4a3a6e;
    }

    .cover-page .cover-ornament {
      color: #c9a84c;
    }

    .cover-page .cover-author {
      color: #1a1a3e;
    }

    .cover-page .cover-publisher,
    .cover-page .cover-year {
      color: #4a3a6e;
    }

    /* Front matter */
    .copyright-page {
      page-break-after: always;
      color: #666;
    }

    .copyright-page .section-label {
      color: #2a2a2a;
    }

    .contents-page {
      page-break-after: always;
    }

    .contents-page h2 {
      color: #c9a84c;
    }

    .contents-chapter .ch-num {
      color: #c9a84c;
    }

    .dedication {
      page-break-after: always;
      color: #4a3a6e;
    }

    /* Part headers */
    .part-header {
      page-break-before: always;
      page-break-after: avoid;
      border-top: 3px solid #c9a84c;
      border-bottom: 1px solid #e0dcd4;
      padding: 50px 0 30px;
    }

    .part-title {
      color: #c9a84c;
    }

    .part-subtitle {
      color: #1a1a3e;
    }

    .part-desc {
      color: #4a3a6e;
    }

    /* Chapters */
    .chapter-section {
      page-break-before: always;
    }

    .chapter-title {
      color: #c9a84c;
    }

    .chapter-subtitle {
      color: #1a1a3e;
    }

    /* Section headings */
    h3.section-heading {
      color: #1a1a3e;
      border-top: 1px solid #e0dcd4;
      page-break-after: avoid;
    }

    h4.subsection-heading {
      color: #4a3a6e;
      page-break-after: avoid;
    }

    /* Blockquotes */
    blockquote {
      border-left: 3px solid #c9a84c;
      background: #f5f0e8;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .epigraph {
      border-left: none;
      background: none;
    }

    .citation {
      color: #4a3a6e;
    }

    /* Separators */
    .separator {
      color: #c9a84c;
    }

    .codex-axiom {
      color: #c9a84c;
    }

    .bold-statement strong {
      color: #1a1a3e;
    }

    /* Images */
    .book-image {
      page-break-inside: avoid;
      text-align: center;
      margin: 30px auto;
    }

    .book-image img {
      max-width: 85%;
      box-shadow: none;
    }

    .book-image figcaption {
      color: #4a3a6e;
    }

    .book-image.frontispiece {
      page-break-after: always;
    }

    .book-image.part-opener {
      page-break-before: always;
    }

    .book-image.closing-image img {
      max-width: 60%;
    }

    /* SAIVAS framework card */
    .framework-container {
      page-break-before: always;
    }

    .framework-container .card {
      box-shadow: none;
      border: 2px solid #c9a84c;
    }
  }
"""

NEW_TOC_CSS = """
  /* TOC Toggle Button */
  .toc-toggle {
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 200;
    background: var(--nav-bg);
    color: var(--gold);
    border: 1px solid var(--gold);
    padding: 8px 16px;
    font-family: Georgia, serif;
    font-size: 14px;
    cursor: pointer;
    border-radius: 4px;
    letter-spacing: 1px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .toc-toggle:hover {
    background: var(--gold);
    color: var(--nav-bg);
  }

  /* TOC Overlay */
  .toc-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 299;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }

  .toc-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }

  /* TOC Drawer */
  .toc-drawer {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    height: 100vh;
    background: var(--nav-bg);
    z-index: 300;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .toc-drawer.open {
    transform: translateX(0);
  }

  .toc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    border-bottom: 1px solid rgba(201, 168, 76, 0.3);
    flex-shrink: 0;
  }

  .toc-header h2 {
    color: var(--gold);
    font-size: 14px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0;
  }

  .toc-close {
    background: none;
    border: none;
    color: var(--gold);
    font-size: 28px;
    cursor: pointer;
    padding: 0 4px;
    line-height: 1;
  }

  .toc-close:hover {
    color: #fff;
  }

  .toc-links {
    flex: 1;
    overflow-y: auto;
    padding: 10px 0;
  }

  .toc-link {
    display: block;
    padding: 8px 24px;
    color: var(--nav-text, #d4cfc5);
    text-decoration: none;
    font-size: 14px;
    transition: all 0.2s;
    border-left: 3px solid transparent;
  }

  .toc-link:hover {
    color: var(--gold);
    background: rgba(201, 168, 76, 0.08);
    border-left-color: var(--gold);
  }

  .toc-part {
    margin-top: 8px;
  }

  .toc-part-title {
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--gold) !important;
    padding: 8px 24px 4px;
  }

  .toc-chapter {
    padding-left: 36px;
    font-size: 13px;
  }

  .toc-footer {
    padding: 15px 20px;
    border-top: 1px solid rgba(201, 168, 76, 0.3);
    flex-shrink: 0;
  }

  /* Download dropdown */
  .download-dropdown {
    position: relative;
  }

  .download-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    padding: 10px 16px;
    background: transparent;
    color: var(--gold);
    border: 1px solid var(--gold);
    font-family: Georgia, serif;
    font-size: 13px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s;
    letter-spacing: 1px;
  }

  .download-btn:hover {
    background: var(--gold);
    color: var(--nav-bg);
  }

  .download-arrow {
    transition: transform 0.2s;
  }

  .download-dropdown.open .download-arrow {
    transform: rotate(180deg);
  }

  .download-menu {
    display: none;
    position: absolute;
    bottom: 100%;
    left: 0;
    right: 0;
    background: var(--nav-bg, #1a1a3e);
    border: 1px solid var(--gold);
    border-radius: 4px;
    margin-bottom: 6px;
    overflow: hidden;
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.3);
  }

  .download-dropdown.open .download-menu {
    display: block;
  }

  .download-option {
    display: block;
    padding: 10px 18px;
    color: var(--nav-text, #d4cfc5);
    text-decoration: none;
    font-family: Georgia, serif;
    font-size: 13px;
    letter-spacing: 0.5px;
    transition: all 0.15s;
    border-bottom: 1px solid rgba(201, 168, 76, 0.15);
  }

  .download-option:last-child {
    border-bottom: none;
  }

  .download-option:hover {
    background: rgba(201, 168, 76, 0.15);
    color: var(--gold);
  }
"""

NEW_TOC_JS = """
  // Download dropdown
  const downloadBtn = document.getElementById('downloadBtn');
  const downloadDropdown = document.getElementById('downloadDropdown');

  downloadBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    downloadDropdown.classList.toggle('open');
  });

  document.addEventListener('click', function(e) {
    if (!downloadDropdown.contains(e.target)) {
      downloadDropdown.classList.remove('open');
    }
  });

  // TOC Drawer toggle
  const tocToggle = document.getElementById('tocToggle');
  const tocDrawer = document.getElementById('tocDrawer');
  const tocOverlay = document.getElementById('tocOverlay');
  const tocClose = document.getElementById('tocClose');

  function openToc() {
    tocDrawer.classList.add('open');
    tocOverlay.classList.add('open');
  }

  function closeToc() {
    tocDrawer.classList.remove('open');
    tocOverlay.classList.remove('open');
  }

  tocToggle.addEventListener('click', openToc);
  tocClose.addEventListener('click', closeToc);
  tocOverlay.addEventListener('click', closeToc);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeToc();
  });

  // Close drawer when clicking a link
  tocDrawer.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      closeToc();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 300);
      }
    });
  });

  // Progress bar
  const progressBar = document.getElementById('progressBar');
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = progress + '%';
  });

  // Scroll to top
  const scrollTopBtn = document.getElementById('scrollTop');
  window.addEventListener('scroll', () => {
    scrollTopBtn.style.display = window.scrollY > 500 ? 'flex' : 'none';
  });
  scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
"""


def extract_css(html_content):
    """Extract the full CSS block from the existing HTML."""
    match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("Could not extract <style> block from existing HTML")


def extract_js(html_content):
    """Extract the full JS block from the existing HTML."""
    match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("Could not extract <script> block from existing HTML")


def extract_framework_card(framework_content):
    """Extract the <div class="card">...</div> from the framework HTML."""
    match = re.search(r'(<div class="card">.*?</div>\s*\n</div>)', framework_content, re.DOTALL)
    if match:
        return match.group(1)
    # Try a more greedy approach - find from <div class="card"> to the last </div> before </body>
    match = re.search(r'(<div class="card">.*)</div>\s*</body>', framework_content, re.DOTALL)
    if match:
        return match.group(1) + "</div>"
    raise ValueError("Could not extract card div from framework HTML")


def parse_frontmatter(lines):
    """Parse YAML frontmatter and return remaining lines."""
    if lines[0].strip() == '---':
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
        if end_idx is not None:
            return lines[end_idx + 1:]
    return lines


def build_toc_drawer() -> str:
    """Build the collapsible table of contents drawer."""
    parts = []
    parts.append('<div class="toc-overlay" id="tocOverlay"></div>')
    parts.append('<nav class="toc-drawer" id="tocDrawer">')
    parts.append('  <div class="toc-header">')
    parts.append('    <h2>Contents</h2>')
    parts.append('    <button class="toc-close" id="tocClose" aria-label="Close">&times;</button>')
    parts.append('  </div>')
    parts.append('  <div class="toc-links">')
    parts.append('  <a href="#cover" class="toc-link">Cover</a>')
    parts.append('  <a href="#copyright" class="toc-link">Copyright</a>')
    parts.append('  <a href="#authors-note" class="toc-link">Author&rsquo;s Note</a>')

    for part_name in ["ONE", "TWO", "THREE", "FOUR", "FIVE"]:
        part_id = PART_NUMBER_TO_ID[part_name]
        parts.append('  <div class="toc-part">')
        parts.append(f'    <a href="#{part_id}" class="toc-link toc-part-title">PART {part_name}</a>')
        for ch in PART_CHAPTERS[part_name]:
            title = CHAPTER_TITLES.get(ch, "")
            label = f"Ch {ch}: {title}" if title else f"Chapter {ch}"
            parts.append(f'    <a href="#chapter-{ch}" class="toc-link toc-chapter">{label}</a>')
        if part_name == "FIVE":
            parts.append('    <a href="#sentient-ai-framework" class="toc-link toc-chapter">SAIVAS Reference Card</a>')
        parts.append('  </div>')

    # Appendices
    parts.append('  <div class="toc-part">')
    parts.append('    <a href="#appendices" class="toc-link toc-part-title">APPENDICES</a>')
    parts.append('    <a href="#appendix-a" class="toc-link toc-chapter">A: SAIVAS Reference Card</a>')
    parts.append('    <a href="#appendix-b" class="toc-link toc-chapter">B: Standards Proposal</a>')
    parts.append('    <a href="#appendix-c" class="toc-link toc-chapter">C: Codex Axioms</a>')
    parts.append('  </div>')

    parts.append('  </div>')
    parts.append('  <div class="toc-footer">')
    parts.append('    <div class="download-dropdown" id="downloadDropdown">')
    parts.append('      <button class="download-btn" id="downloadBtn">')
    parts.append('        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>')
    parts.append('        <span>Download</span>')
    parts.append('        <svg class="download-arrow" viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>')
    parts.append('      </button>')
    parts.append('      <div class="download-menu" id="downloadMenu">')
    parts.append('        <a href="Uniform_Gnosis_Volume_I.html" download class="download-option">HTML</a>')
    parts.append('        <a href="Uniform_Gnosis_Volume_I.pdf" download class="download-option">PDF</a>')
    parts.append('        <a href="Uniform_Gnosis_Volume_I.epub" download class="download-option">EPUB</a>')
    parts.append('        <a href="Uniform_Gnosis_Volume_I.md" download class="download-option">Markdown</a>')
    parts.append('      </div>')
    parts.append('    </div>')
    parts.append('  </div>')
    parts.append('</nav>')
    return '\n'.join(parts)


def build_cover_page():
    """Build the cover page HTML."""
    return """<div id="cover" class="cover-page">
    <p class="series-title">The Spiritual Codex</p>
    <p class="volume-label">Volume I</p>
    <h1>Uniform Gnosis</h1>
    <p class="cover-subtitle">The Architecture of Reality</p>
    <p class="cover-ornament">&#10022; &#10022; &#10022;</p>
    <p class="cover-author">Daniel Medina</p>
    <p class="cover-publisher">Uniformedi LLC</p>
    <p class="cover-year">2026</p>
</div>"""


def build_contents_page(lines):
    """Build the contents page from the CONTENTS section in markdown."""
    html_parts = []
    html_parts.append('<div id="contents" class="contents-page">')
    html_parts.append('<h2>Contents</h2>')

    current_part = None
    chapter_num = 0

    for line in lines:
        line = line.strip()
        # Part title line like **PART ONE: THE SOURCE CODE**
        part_match = re.match(r'\*\*PART\s+(ONE|TWO|THREE|FOUR|FIVE):\s*(.*?)\*\*', line)
        if part_match:
            if current_part is not None:
                html_parts.append('</div>')  # close previous contents-part
            part_word = part_match.group(1)
            part_title = part_match.group(2)
            part_id = PART_NUMBER_TO_ID[part_word]
            html_parts.append(f'<div class="contents-part">')
            html_parts.append(f'<div class="contents-part-title"><a href="#{part_id}" style="color: inherit; text-decoration: none;">Part {part_word}: {part_title}</a></div>')
            current_part = part_word
            continue

        # Chapter entry like "  - Chapter 1: Title"
        ch_match = re.match(r'\s*-\s*Chapter\s+(\d+):\s*(.*)', line)
        if ch_match:
            ch_num = ch_match.group(1)
            ch_title = ch_match.group(2)
            # Convert em-dashes
            ch_title = ch_title.replace('—', '&mdash;')
            html_parts.append(f'<a href="#chapter-{ch_num}" class="contents-chapter"><span class="ch-num">Chapter {ch_num}</span> {ch_title}</a>')
            continue

    if current_part is not None:
        html_parts.append('</div>')  # close last contents-part

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def convert_inline(text):
    """Convert inline markdown formatting to HTML."""
    # Bold + italic: ***text***
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Links: [text](url)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    return text


def get_image_class(img_path, chapter_started, is_last_image):
    """Determine the CSS class for an image based on context."""
    if is_last_image:
        return "book-image closing-image"
    if img_path == FRONTISPIECE_IMAGE:
        return "book-image frontispiece"
    if not chapter_started or img_path in PART_OPENER_IMAGES:
        return "book-image part-opener"
    return "book-image"


def convert_md_to_html(md_content, css_content, js_content, framework_card):
    """Main conversion function."""
    lines = md_content.split('\n')

    # Skip frontmatter
    lines = parse_frontmatter(lines)

    # Collect all image paths to identify the last one
    all_images = []
    for line in lines:
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', line.strip())
        if img_match:
            all_images.append(img_match.group(2))
    last_image = all_images[-1] if all_images else None

    # State tracking
    in_title_page = False
    in_copyright_page = False
    in_dedication = False
    in_authors_note = False
    in_contents = False
    in_chapter = False
    in_part = False
    in_blockquote = False
    chapter_started = False  # True once we've seen Chapter 1
    current_chapter = 0
    epigraph_done = False
    contents_lines = []
    pending_subtitle_lines = 0  # How many italic subtitle lines to expect after chapter heading
    just_saw_chapter_heading = False
    just_saw_part_heading = False
    part_subtitle_count = 0

    content_parts = []

    def close_open_sections():
        """Close any open chapter section or part container."""
        nonlocal in_chapter, in_part
        result = []
        if in_chapter:
            result.append('</section>')
            in_chapter = False
        if in_part:
            result.append('</div>')  # close part-container
            in_part = False
        return result

    # Build content
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip horizontal rules (---)
        if stripped == '---':
            i += 1
            continue

        # Handle raw HTML div blocks
        if stripped == '<div class="title-page">':
            in_title_page = True
            i += 1
            continue

        if stripped == '</div>' and in_title_page:
            in_title_page = False
            content_parts.append(build_cover_page())
            i += 1
            continue

        if in_title_page:
            i += 1
            continue

        if stripped == '<div class="copyright-page">':
            in_copyright_page = True
            content_parts.append('<div id="copyright" class="copyright-page">')
            i += 1
            continue

        if stripped == '</div>' and in_copyright_page:
            in_copyright_page = False
            content_parts.append('</div>')
            i += 1
            continue

        if in_copyright_page:
            if not stripped:
                i += 1
                continue
            # Bold labels become section-label
            bold_match = re.match(r'^\*\*(.*?)\*\*$', stripped)
            if bold_match:
                label_text = bold_match.group(1)
                content_parts.append(f'<p class="section-label">{label_text}</p>')
            else:
                content_parts.append(f'<p>{convert_inline(stripped)}</p>')
            i += 1
            continue

        if stripped == '<div class="dedication">':
            in_dedication = True
            content_parts.append('<div class="dedication">')
            i += 1
            continue

        if stripped == '</div>' and in_dedication:
            in_dedication = False
            content_parts.append('</div>')
            i += 1
            continue

        if in_dedication:
            if stripped:
                # Remove surrounding *...*
                ded_match = re.match(r'^\*(.*?)\*$', stripped)
                if ded_match:
                    content_parts.append(f'<p><em>{ded_match.group(1)}</em></p>')
                else:
                    content_parts.append(f'<p>{convert_inline(stripped)}</p>')
            i += 1
            continue

        # Blockquote epigraph (before Author's Note)
        if stripped.startswith('> ') and not epigraph_done and not in_chapter:
            # Collect all blockquote lines
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                bq_lines.append(lines[i].strip()[2:])  # Remove "> "
                i += 1

            # Separate quote from attribution
            quote_lines = []
            attribution = None
            for bq_line in bq_lines:
                if bq_line.startswith('\u2014 ') or bq_line.startswith('— '):
                    attribution = bq_line
                else:
                    # Strip surrounding *...*
                    bq_clean = re.sub(r'^\*"?(.*?)"?\*$', r'\1', bq_line)
                    bq_clean = re.sub(r'^\*(.*?)\*$', r'\1', bq_line)
                    quote_lines.append(bq_clean)

            quote_text = ' '.join(quote_lines)
            # Clean up italic markers
            quote_text = re.sub(r'^\*', '', quote_text)
            quote_text = re.sub(r'\*$', '', quote_text)

            content_parts.append('<blockquote class="epigraph">')
            content_parts.append(f'<p><em>{quote_text}</em></p>')
            if attribution:
                content_parts.append(f'<footer>{attribution}</footer>')
            content_parts.append('</blockquote>')
            epigraph_done = True
            continue

        # AUTHOR'S NOTE section
        if stripped == "## AUTHOR'S NOTE" or stripped == "## AUTHOR\u2019S NOTE":
            in_authors_note = True
            in_contents = False
            content_parts.append('<section id="authors-note" class="chapter-section">')
            content_parts.append('<h2 class="chapter-title">Author&rsquo;s Note</h2>')
            i += 1
            continue

        # CONTENTS section
        if stripped == '## CONTENTS':
            if in_authors_note:
                content_parts.append('</section>')
                in_authors_note = False
            in_contents = True
            contents_lines = []
            i += 1
            continue

        if in_contents:
            # Contents ends when we hit the actual part heading (not a TOC entry)
            # This can be **PART ONE** (bold) or # PART ONE (h1 heading)
            if re.match(r'^(#\s+|\*\*)PART\s+(ONE|TWO|THREE|FOUR|FIVE)(\*\*)?$', stripped):
                # This is the actual part heading, not a TOC entry
                in_contents = False
                # Emit the contents page
                content_parts.append(build_contents_page(contents_lines))
                # Now handle this as a part heading - fall through below
            elif re.match(r'^\*\*PART\s+(ONE|TWO|THREE|FOUR|FIVE):\s*', stripped):
                # This is a TOC entry
                contents_lines.append(line)
                i += 1
                continue
            elif re.match(r'\s*-\s*Chapter', stripped):
                contents_lines.append(line)
                i += 1
                continue
            else:
                # Blank line in contents, skip
                if not stripped:
                    i += 1
                    continue
                # Otherwise check if it's a part heading
                if not re.match(r'^\*\*PART', stripped):
                    i += 1
                    continue

        if in_authors_note:
            if stripped.startswith('## '):
                # End of author's note
                content_parts.append('</section>')
                in_authors_note = False
                # Don't increment i, reprocess this line
                continue
            if not stripped:
                i += 1
                continue
            content_parts.append(f'<p>{convert_inline(stripped)}</p>')
            i += 1
            continue

        # PART headings: either `# PART X` or `**PART X**`
        part_match_h1 = re.match(r'^#\s+PART\s+(ONE|TWO|THREE|FOUR|FIVE)$', stripped)
        part_match_bold = re.match(r'^\*\*PART\s+(ONE|TWO|THREE|FOUR|FIVE)\*\*$', stripped)

        if part_match_h1 or part_match_bold:
            match = part_match_h1 or part_match_bold
            part_word = match.group(1)
            part_id = PART_NUMBER_TO_ID[part_word]

            # Close previous sections
            content_parts.extend(close_open_sections())

            part_title, part_desc = PART_TITLES[part_word]

            content_parts.append(f'<div id="{part_id}" class="part-container">')
            content_parts.append('<div class="part-header">')
            content_parts.append(f'<h2 class="part-title">PART {part_word}</h2>')
            content_parts.append(f'<p class="part-subtitle"><em>{part_title}</em></p>')
            if part_desc:
                content_parts.append(f'<p class="part-desc"><em>{part_desc}</em></p>')
            content_parts.append('</div>')

            in_part = True
            just_saw_part_heading = True
            part_subtitle_count = 0

            # Skip the next lines that are part subtitle/desc (### *Title* and *Subtitle*)
            i += 1
            while i < len(lines):
                next_stripped = lines[i].strip()
                if not next_stripped:
                    i += 1
                    continue
                # Skip ### *Title* lines and *Subtitle* lines for parts
                if re.match(r'^###\s+\*.*\*$', next_stripped):
                    i += 1
                    continue
                if re.match(r'^\*[^*].*\*$', next_stripped) and not next_stripped.startswith('*—'):
                    i += 1
                    continue
                break
            continue

        # APPENDICES section header: # APPENDICES
        if stripped == '# APPENDICES':
            content_parts.extend(close_open_sections())
            content_parts.append('<div id="appendices" class="part-container">')
            content_parts.append('<div class="part-header">')
            content_parts.append('<h2 class="part-title">APPENDICES</h2>')
            content_parts.append('</div>')
            in_part = True
            i += 1
            continue

        # Appendix headings: ## APPENDIX A/B/C
        app_match = re.match(r'^##\s+APPENDIX\s+([A-C])$', stripped)
        if app_match:
            app_letter = app_match.group(1)
            if in_chapter:
                content_parts.append('</section>')
                in_chapter = False
            content_parts.append(f'<section id="appendix-{app_letter.lower()}" class="chapter-section">')
            content_parts.append(f'<h2 class="chapter-title">APPENDIX {app_letter}</h2>')
            in_chapter = True
            i += 1
            # Consume subtitle lines
            while i < len(lines):
                next_stripped = lines[i].strip()
                if not next_stripped:
                    i += 1
                    continue
                italic_match = re.match(r'^\*(.*?)\*$', next_stripped)
                if italic_match and not next_stripped.startswith('*"') and not next_stripped.startswith('*\u201c'):
                    subtitle_text = italic_match.group(1)
                    content_parts.append(f'<p class="chapter-subtitle"><em>{subtitle_text}</em></p>')
                    i += 1
                    continue
                break
            continue

        # Chapter headings: ## CHAPTER N
        ch_match = re.match(r'^##\s+CHAPTER\s+(\d+)$', stripped)
        if ch_match:
            ch_num = int(ch_match.group(1))
            current_chapter = ch_num

            # Close previous chapter section
            if in_chapter:
                content_parts.append('</section>')
                in_chapter = False

            if not chapter_started:
                chapter_started = True

            content_parts.append(f'<section id="chapter-{ch_num}" class="chapter-section">')
            content_parts.append(f'<h2 class="chapter-title">CHAPTER {ch_num}</h2>')
            in_chapter = True
            just_saw_chapter_heading = True

            i += 1
            # Consume following subtitle lines (italic lines right after chapter heading)
            while i < len(lines):
                next_stripped = lines[i].strip()
                if not next_stripped:
                    i += 1
                    continue
                italic_match = re.match(r'^\*(.*?)\*$', next_stripped)
                if italic_match and not next_stripped.startswith('*"') and not next_stripped.startswith('*\u201c') and not next_stripped.startswith('*\u2014') and not next_stripped.startswith('*\u2019'):
                    subtitle_text = italic_match.group(1)
                    content_parts.append(f'<p class="chapter-subtitle"><em>{subtitle_text}</em></p>')
                    i += 1
                    continue
                break
            just_saw_chapter_heading = False
            continue

        # Section headings: ### Heading
        h3_match = re.match(r'^###\s+(.*)', stripped)
        if h3_match and in_chapter:
            heading_text = h3_match.group(1)
            # Remove italic markers if present
            heading_text = re.sub(r'^\*(.*)\*$', r'\1', heading_text)
            content_parts.append(f'<h3 class="section-heading">{convert_inline(heading_text)}</h3>')
            i += 1
            continue

        # Subsection headings: #### Heading
        h4_match = re.match(r'^####\s+(.*)', stripped)
        if h4_match and in_chapter:
            heading_text = h4_match.group(1)
            content_parts.append(f'<h4 class="subsection-heading">{convert_inline(heading_text)}</h4>')
            i += 1
            continue

        # Separator: <p class="separator">...</p>
        if '<p class="separator">' in stripped:
            content_parts.append(stripped)
            i += 1
            continue

        # Images: ![alt](path)
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)

            is_last = (img_path == last_image)
            img_class = get_image_class(img_path, chapter_started, is_last)

            # Check next non-empty line for caption
            caption = None
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                cap_match = re.match(r'^\*(.*?)\*$', lines[j].strip())
                if cap_match:
                    caption = cap_match.group(1)
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1

            content_parts.append(f'<figure class="{img_class}">')
            content_parts.append(f'<img src="{img_path}" alt="{alt_text}">')
            if caption:
                content_parts.append(f'<figcaption>{caption}</figcaption>')
            content_parts.append('</figure>')
            continue

        # Blockquote within chapters (> lines)
        if stripped.startswith('> ') and in_chapter:
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                bq_lines.append(lines[i].strip()[2:])
                i += 1

            quote_lines = []
            attribution = None
            for bq_line in bq_lines:
                if bq_line.startswith('\u2014 ') or bq_line.startswith('— '):
                    attribution = bq_line
                else:
                    quote_lines.append(bq_line)

            content_parts.append('<blockquote>')
            for ql in quote_lines:
                content_parts.append(f'<p>{convert_inline(ql)}</p>')
            content_parts.append('</blockquote>')
            if attribution:
                content_parts.append(f'<p class="citation">{attribution}</p>')
            continue

        # Codex Axiom: **Codex Axiom**
        if stripped == '**Codex Axiom**':
            content_parts.append('<p class="codex-axiom">Codex Axiom</p>')
            i += 1
            continue

        # Bold statement: **Bold Text** (entire line is bold)
        bold_match = re.match(r'^\*\*(.*?)\*\*$', stripped)
        if bold_match and stripped != '**Codex Axiom**':
            bold_text = bold_match.group(1)
            # Check if this is "End of Volume I" type text
            content_parts.append(f'<p class="bold-statement"><strong>{bold_text}</strong></p>')
            i += 1
            continue

        # Standalone italic paragraph (not a subtitle consumed above)
        italic_match = re.match(r'^\*(.*?)\*$', stripped)
        if italic_match and stripped not in ('*', '**'):
            italic_text = italic_match.group(1)
            # Attribution/citation style
            if italic_text.startswith('\u2014 ') or italic_text.startswith('— '):
                content_parts.append(f'<p class="citation"><em>{italic_text}</em></p>')
            else:
                content_parts.append(f'<p><em>{italic_text}</em></p>')
            i += 1
            continue

        # Italic lines that span multiple lines (start with * but don't end with *)
        if stripped.startswith('*') and not stripped.startswith('**') and not stripped.endswith('*'):
            # Multi-line italic - collect until closing *
            collected = stripped
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    break
                collected += ' ' + next_line
                i += 1
                if next_line.endswith('*'):
                    break
            # Remove surrounding * markers
            collected = re.sub(r'^\*', '', collected)
            collected = re.sub(r'\*$', '', collected)
            content_parts.append(f'<p><em>{collected}</em></p>')
            continue

        # Attribution lines starting with em-dash (not in italic)
        if stripped.startswith('\u2014 ') or stripped.startswith('— '):
            content_parts.append(f'<p class="citation">{stripped}</p>')
            i += 1
            continue

        # Chapter 13 special: bare "SAIVAS" heading after ## CHAPTER 13
        # These are plain text that should be section headings
        # Handle as regular paragraph

        # Empty lines
        if not stripped:
            i += 1
            continue

        # Regular paragraph
        content_parts.append(f'<p>{convert_inline(stripped)}</p>')
        i += 1

    # Close any remaining open sections
    content_parts.extend(close_open_sections())

    return '\n'.join(content_parts)


def build_html(css: str, js: str, main_content: str, framework_card: str) -> str:
    """Assemble the complete HTML document."""
    toc_drawer = build_toc_drawer()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Spiritual Codex &mdash; Volume I: Uniform Gnosis</title>

<style>
{css}
</style>
</head>
<body id="top">

<div class="progress-bar"><div class="progress-bar-fill" id="progressBar"></div></div>

<button class="toc-toggle" id="tocToggle" aria-label="Open table of contents">&#9776; Contents</button>

{toc_drawer}

<div class="main-content">

{main_content}

<!-- SAIVAS Reference Card -->
<div class="framework-container" id="sentient-ai-framework">
{framework_card}
</div>

</div>

<button class="scroll-top" id="scrollTop" title="Scroll to top">&uarr;</button>

<script>
{js}
</script>

</body>
</html>"""
    return html


def main() -> None:
    """Main entry point."""
    # Read input files
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    with open(FRAMEWORK_FILE, 'r', encoding='utf-8') as f:
        framework_content = f.read()

    # Extract CSS and framework card from existing HTML
    css = extract_css(html_content)
    framework_card = extract_framework_card(framework_content)

    # Modify CSS: change main-content from sidebar layout to centered
    css = css.replace('margin-left: var(--nav-width);', 'margin-left: auto; margin-right: auto;')
    css = css.replace('left: var(--nav-width);', 'left: 0;')
    css = css.replace('width: calc(100% - var(--nav-width));', 'width: 100%;')

    # Replace plain print CSS with styled print CSS
    css = re.sub(
        r'@media print \{[^}]*\.sidebar.*?\}',
        PRINT_CSS_REPLACEMENT,
        css,
        flags=re.DOTALL,
    )

    # Append new TOC drawer CSS
    css += NEW_TOC_CSS

    # Use new JS (not extracted from old HTML)
    js = NEW_TOC_JS

    # Convert markdown to HTML content
    main_content = convert_md_to_html(md_content, css, js, framework_card)

    # Build complete HTML
    output = build_html(css, js, main_content, framework_card)

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    file_size = os.path.getsize(OUTPUT_FILE)
    print(f"Generated {OUTPUT_FILE}")
    print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")


if __name__ == '__main__':
    main()
