#!/usr/bin/env python3
"""
Content Generator for Lecture Materials

This script generates content for lectures, including:
- Rendered lecture pages
- Slides (HTML and PDF formats)
- Jupyter notebooks

Special tags for content filtering:
- <!-- RENDER: --> ... <!-- end RENDER: -->
- <!-- SLIDES: --> ... <!-- end SLIDES: -->
- <!-- NOTEBOOK: --> ... <!-- end NOTEBOOK: -->
- <!-- ALL: --> ... <!-- end ALL: --> (included in all formats)

PDF slide optimization:
- Add <!-- PDF --> anywhere inside a slide to mark it for inclusion in the PDF output
- Only slides marked with this comment will be included in the PDF
- All slides are always included in the HTML output
- The title slide and final "Thank you" slide are automatically included in the PDF
- This optimization helps reduce PDF file size and generation time

Example usage:
```python
#!/usr/bin/env python3
import os
from scripts.generate_content import ContentGenerator

generator = ContentGenerator(os.getcwd())
generator.process_lecture("course_code/lecture_name.md")
```

or from the command line (run from repo root):
```
python scripts/generate_content/generate_content.py course_code/lecture_name
python scripts/generate_content/generate_content.py --slides-only course_code/lecture_name
```

Optional talk front matter for **internal** talks (``type: internal``) title slide:

- **Multi-line title:** use a YAML block string (``title_slide: |``) with one line per title line, or put ``@NL@`` in a single-line string to mark a line break. Colons in the title do **not** trigger a split.

Optional talk front matter (non-internal) for the closing **Many Thanks** slide:

- ``thanks_slides_qr: true`` — show a QR code (slides URL), then **Many Thanks!**, then optional website and email lines.
- ``thanks_website_url`` — full URL shown as a link under the title (omit to skip that line).
- ``thanks_qr_target_url`` — optional; if set, the QR encodes this URL instead of the default ``{site}/assets/slides/{year}/{source_stem}.html``.
- ``thanks_extended`` — alias for ``thanks_slides_qr`` if you prefer the name.
"""
import os
import re
import yaml
import subprocess
import shutil
from pathlib import Path
import nbformat as nbf
import magic
from PIL import Image
import mimetypes
import requests
from urllib.parse import urlparse, quote
from html import escape
import argparse

class ContentGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.sources_dir = self.base_dir / "scripts" / "generate_content" / "lectures-sources"
        self.talks_sources_dir = self.base_dir / "scripts" / "generate_content" / "talks-sources"
        self.lectures_dir = self.base_dir / "content" / "_lectures"
        self.talks_dir = self.base_dir / "content" / "_talks"
        self.data_dir = self.base_dir / "_data"
        self.assets_dir = self.base_dir / "assets"
        self.media_dir = self.base_dir / "assets" / "media"

        # Create output directories
        self.lectures_dir.mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "slides").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "notebooks").mkdir(parents=True, exist_ok=True)
        (self.media_dir).mkdir(parents=True, exist_ok=True)

        # Initialize mime type detector
        self.mime = magic.Magic(mime=True)

    def get_course_metadata(self, course_code):
        """Get course metadata from the course file."""
        course_file = self.base_dir / "content" / "_courses" / f"{course_code}.md"
        if not course_file.exists():
            print(f"Warning: Course file {course_file} not found")
            return {}

        with open(course_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract front matter
        front_matter = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not front_matter:
            return {}

        return yaml.safe_load(front_matter.group(1))

    def load_talks_data(self):
        """Load talks list from _data/talks.yml."""
        talks_file = self.data_dir / "talks.yml"
        if not talks_file.exists():
            return []
        with open(talks_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, list) else []

    # Keys allowed in talks.yml (talk-only metadata; do not mix in lecture-only fields)
    TALK_YML_KEYS = (
        'talk_id', 'title', 'conference', 'venue', 'institution', 'location',
        'year', 'month', 'date', 'type', 'status', 'visible', 'slides', 'page'
    )

    def update_talks_yml(self, talks_list):
        """Write updated talks list back to _data/talks.yml."""
        talks_file = self.data_dir / "talks.yml"
        with open(talks_file, 'w', encoding='utf-8') as f:
            yaml.dump(talks_list, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def get_site_base_url(self):
        """Site origin from _config.yml ``url`` (for absolute slide and page links)."""
        config_file = self.base_dir / "_config.yml"
        base_url = "https://cabrerac.github.io"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as cf:
                config_content = cf.read()
            url_match = re.search(r'^\s*url:\s*["\']([^"\']+)["\']', config_content, re.MULTILINE)
            if url_match:
                base_url = url_match.group(1).strip().rstrip('/')
        return base_url

    def resolve_public_slides_url(self, metadata, file_stem):
        """Absolute deployed slides URL; output file is always ``<file_stem>.html`` (needs ``year``)."""
        year = metadata.get('year')
        if year is None:
            return None
        base = self.get_site_base_url()
        return f"{base}/assets/slides/{int(year)}/{file_stem}.html".strip()

    def read_snippet(self, snippet_path):
        """Read a snippet file and return its content."""
        with open(snippet_path, 'r', encoding='utf-8') as f:
            return f.read()

    def process_media(self, content):
        """Process media content in markdown and handle media files from assets."""
        # Find all media references in markdown
        media_patterns = [
            r'!\[(.*?)\]\((.*?)\)',  # Images
            r'<video.*?src="(.*?)".*?>',  # Videos
            r'<audio.*?src="(.*?)".*?>',  # Audio
        ]

        processed_content = content
        for pattern in media_patterns:
            for match in re.finditer(pattern, content):
                media_path = match.group(2)
                # Check if the path is already in assets/media
                if media_path.startswith('/assets/media/'):
                    continue

                # Look for the media file in assets/media
                media_name = Path(media_path).name
                media_type = None

                # Try to find the file in assets/media
                for media_type_dir in self.media_dir.iterdir():
                    if media_type_dir.is_dir():
                        media_file = media_type_dir / media_name
                        if media_file.exists():
                            media_type = media_type_dir.name
                            break

                if media_type:
                    # Update content with the correct path
                    relative_path = f"/assets/media/{media_type}/{media_name}"
                    processed_content = processed_content.replace(media_path, relative_path)
                else:
                    print(f"Warning: Media file {media_name} not found in assets/media")

        return processed_content

    def verify_colab_link(self, colab_link):
        """Verify if a Colab notebook link is accessible."""
        try:
            # Convert Colab link to raw GitHub content URL
            parsed_url = urlparse(colab_link)
            path_parts = parsed_url.path.split('/')
            if len(path_parts) >= 7:  # Ensure we have enough path components
                owner = path_parts[2]
                repo = path_parts[3]
                file_path = '/'.join(path_parts[6:])

                # Use gh-pages branch
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/gh-pages/{file_path}"

                # Make HEAD request to check if file exists
                response = requests.head(raw_url, allow_redirects=True)
                return response.status_code == 200
        except Exception as e:
            print(f"Error verifying Colab link: {e}")
            return False
        return False

    def check_marp_installation(self):
        """Check Marp CLI installation and PATH configuration."""
        print("\nChecking Marp CLI installation...")

        # First check if npm is available
        try:
            # Try to find npm in common Windows locations
            npm_paths = [
                'npm',
                'npm.cmd',
                os.path.join(os.environ.get('ProgramFiles', ''), 'nodejs', 'npm.cmd'),
                os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'nodejs', 'npm.cmd'),
                os.path.join(os.environ.get('APPDATA', ''), 'npm', 'npm.cmd'),
            ]

            npm_cmd = None
            for path in npm_paths:
                if shutil.which(path):
                    npm_cmd = path
                    break

            if not npm_cmd:
                print("[WARN] npm not found in PATH")
                print("\nPlease install Node.js and npm:")
                print("1. Download Node.js from https://nodejs.org/")
                print("2. Run the installer")
                print("3. Check 'Add to PATH' during installation")
                print("4. Restart your terminal after installation")
                return False

            print(f"[OK] Found npm at: {npm_cmd}")

            # Check npm global installation
            try:
                npm_prefix = subprocess.check_output([npm_cmd, 'config', 'get', 'prefix'], text=True).strip()
                print(f"[OK] npm global prefix: {npm_prefix}")

                # Check if Marp is installed globally
                try:
                    marp_version = subprocess.check_output([npm_cmd, 'list', '-g', '@marp-team/marp-cli'], text=True)
                    print("[OK] Marp CLI is installed globally")
                    print(f"  Installation details:\n{marp_version}")
                except subprocess.CalledProcessError:
                    print("[WARN] Marp CLI is not installed globally")
                    print("\nPlease install Marp CLI:")
                    print(f"1. Run: {npm_cmd} install -g @marp-team/marp-cli")
                    print("2. Restart your terminal after installation")
                    return False

                # Check common Marp locations
                marp_locations = [
                    os.path.join(npm_prefix, 'bin', 'marp'),
                    os.path.join(npm_prefix, 'bin', 'marp.cmd'),
                    os.path.join(os.environ.get('APPDATA', ''), 'npm', 'marp.cmd'),
                    os.path.join(os.path.expanduser('~'), '.npm-global', 'bin', 'marp'),
                    os.path.join(os.path.expanduser('~'), '.npm-global', 'bin', 'marp.cmd'),
                ]

                print("\nChecking Marp executable locations:")
                found = False
                for location in marp_locations:
                    if os.path.exists(location):
                        print(f"[OK] Found Marp at: {location}")
                        found = True
                    else:
                        print(f"[--] Not found: {location}")

                if not found:
                    print("\n[WARN] Marp executable not found in common locations")
                    print(f"  Try running: {npm_cmd} install -g @marp-team/marp-cli")
                    return False

                # Check PATH
                print("\nChecking PATH environment variable:")
                path_dirs = os.environ['PATH'].split(os.pathsep)
                npm_bin_dirs = [
                    os.path.join(npm_prefix, 'bin'),
                    os.path.join(os.environ.get('APPDATA', ''), 'npm'),
                    os.path.join(os.path.expanduser('~'), '.npm-global', 'bin'),
                ]

                for dir_path in npm_bin_dirs:
                    if dir_path in path_dirs:
                        print(f"[OK] npm bin directory in PATH: {dir_path}")
                    else:
                        print(f"[--] npm bin directory not in PATH: {dir_path}")
                        print("  You may need to add this to your PATH")

                # Try running marp directly
                try:
                    marp_version = subprocess.check_output(['marp', '--version'], text=True)
                    print(f"\n[OK] Marp CLI is accessible: {marp_version.strip()}")
                    return True
                except:
                    print("\n[WARN] Marp CLI is not accessible from PATH")
                    print("  Try restarting your terminal or adding the npm bin directory to PATH")
                    return False

            except subprocess.CalledProcessError as e:
                print(f"Error checking npm configuration: {e}")
                print("Make sure npm is installed and in your PATH")
                return False

        except Exception as e:
            print(f"Error: {e}")
            print("\nPlease ensure Node.js and npm are properly installed:")
            print("1. Download and install Node.js from https://nodejs.org/")
            print("2. Make sure to check 'Add to PATH' during installation")
            print("3. Restart your terminal")
            print("4. Verify installation by running 'node --version' and 'npm --version'")
            return False

    def process_includes(self, content, processed_includes=None, depth=0):
        """Process include statements in the content with recursion protection."""
        # Initialize processed_includes set if not provided
        if processed_includes is None:
            processed_includes = set()

        # Maximum recursion depth to prevent infinite loops
        MAX_DEPTH = 10
        if depth > MAX_DEPTH:
            print(f"Warning: Maximum include depth ({MAX_DEPTH}) exceeded. Stopping recursion.")
            return content

        # Maximum number of times the same include can be processed
        MAX_INCLUDE_COUNT = 5

        # Pattern to match include statements
        include_pattern = r'{%\s*include\s+([^%}]+)\s*%}'

        def replace_include(match):
            include_path = match.group(1).strip()
            # Remove quotes if present
            include_path = include_path.strip('"\'')

            # Count total times this include has been processed
            total_include_count = sum(1 for x in processed_includes if x.startswith(f"{include_path}:"))

            # Check if this include has been processed too many times globally (prevent infinite loops)
            if total_include_count >= MAX_INCLUDE_COUNT:
                print(f"Warning: Include {include_path} has been processed {total_include_count} times. Stopping to prevent infinite loops.")
                return match.group(0)  # Return the original include statement

            # Create a unique identifier for this specific include instance
            include_id = f"{include_path}:{depth}:{total_include_count}"

            # Add to processed set
            processed_includes.add(include_id)

            # Look for the include file in _includes
            include_file = self.base_dir / "_includes" / include_path
            if not include_file.exists():
                print(f"Warning: Include file {include_file} not found")
                return match.group(0)

            # Read and process the include file
            with open(include_file, 'r', encoding='utf-8') as f:
                include_content = f.read()

            # Process Liquid template variables
            # Replace {{ site.url }} with the actual site URL for local images
            site_url = "https://cabrerac.github.io"  # Replace with your actual site URL
            include_content = include_content.replace('{{ site.url }}', site_url)

            # Process nested includes with increased depth
            include_content = self.process_includes(include_content, processed_includes, depth + 1)

            # Handle SVG content
            if '<svg' in include_content:
                # Find SVG content
                svg_pattern = r'(<svg.*?</svg>)'
                def format_svg(match):
                    svg_content = match.group(1)
                    # Use Marp's HTML directive
                    return f'<div class="timeline-container">\n{svg_content}\n</div>'

                include_content = re.sub(svg_pattern, format_svg, include_content, flags=re.DOTALL)

            return include_content

        # Replace all include statements
        processed_content = re.sub(include_pattern, replace_include, content)

        return processed_content

    def filter_content(self, content, target):
        """Filter content based on markers for specific target (RENDER, SLIDES, or NOTEBOOK), supporting explicit closing tags and all tag combinations. Deduplicate blocks and preserve order."""
        # Remove front matter first
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Normalize target for case-insensitive matching
        target = target.upper()

        # Regex to match any tag block, capturing the tag(s) and the content
        tag_block_pattern = re.compile(r'<!--\s*([A-Z0-9\+]+):\s*-->(.*?)<!--\s*end [A-Z0-9\+]+:\s*-->', re.DOTALL | re.IGNORECASE)

        filtered_content = []
        seen_blocks = set()

        # Find all matches
        matches = list(tag_block_pattern.finditer(content_without_frontmatter))

        # Iterate sequentially through the content
        for match in matches:
            tag_combo = match.group(1)
            block_content = match.group(2).strip()
            tags = [t.strip().upper() for t in tag_combo.split('+')]

            if 'ALL' in tags or target in tags:
                if block_content and block_content not in seen_blocks:
                    filtered_content.append(block_content)
                    seen_blocks.add(block_content)

        return '\n\n'.join(filtered_content)

    def check_pdf_slide(self, slide_content):
        """Check if a slide should be included in the PDF output based on marker."""
        # Look for the PDF marker in the slide (in any case, with or without spaces)
        pdf_patterns = ["<!-- PDF -->", "<!--PDF-->", "<!-- pdf -->", "<!--pdf-->"]
        return any(pattern in slide_content for pattern in pdf_patterns)

    @staticmethod
    def split_filtered_content_into_slide_blocks(filtered_content):
        """
        Split SLIDES-filtered markdown into one block per slide.

        Slide boundaries are lines that look like Marp headings: '# ' or '## ' at the
        start of the line (after stripping leading whitespace only for the heading test).

        Lines that look like headings inside fenced code blocks (``` ... ```) are not
        boundaries, so examples containing '# ' or '## ' do not start a new slide.
        """
        slide_blocks = []
        current_block = []
        in_fence = False
        for line in filtered_content.split('\n'):
            stripped = line.strip()
            is_slide_boundary = not in_fence and bool(
                re.match(r'^#{1,2} ', stripped)
            )
            if is_slide_boundary and current_block:
                slide_blocks.append('\n'.join(current_block))
                current_block = []
            current_block.append(line)
            if stripped.startswith('```'):
                in_fence = not in_fence
        if current_block:
            slide_blocks.append('\n'.join(current_block))
        return slide_blocks

    @staticmethod
    def _inner_looks_like_tex_math(inner: str) -> bool:
        """Heuristic: TeX math vs currency like $5 (no closing $)."""
        if "$$" in inner:
            return True
        return bool(re.search(r"\$\$|\$[^\$\s\d]", inner))

    def unwrap_html_paragraphs_for_marp_math(self, content):
        """
        Marp does not run MathJax on text inside raw HTML <p>...</p>. For slide sources,
        rewrite those tags into plain markdown paragraphs when the inner HTML looks like
        it contains TeX ($...$ or $$...$$). Authors can then write math inside <p> naturally.

        Fenced ``` blocks are left unchanged. Only used on the slide (Marp) pipeline.
        """
        import re

        fence_re = re.compile(r"(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$")
        placeholders = []

        def extract_fences(text):
            parts = []
            pos = 0
            for m in fence_re.finditer(text):
                parts.append(text[pos:m.start()])
                i = len(placeholders)
                placeholders.append(m.group(0))
                parts.append(f"<<UNWRAPPFENCE{i}>>")
                pos = m.end()
            parts.append(text[pos:])
            return "".join(parts)

        text = extract_fences(content)
        p_tag = re.compile(r"<p\b[^>]*>(.*?)</p>", re.DOTALL | re.IGNORECASE)

        def repl(m):
            inner = m.group(1)
            if "<p" in inner.lower():
                return m.group(0)
            if not self._inner_looks_like_tex_math(inner):
                return m.group(0)
            return f"\n\n{inner.strip()}\n\n"

        text = p_tag.sub(repl, text)
        for i in range(len(placeholders) - 1, -1, -1):
            text = text.replace(f"<<UNWRAPPFENCE{i}>>", placeholders[i])
        return text

    def dedent_indented_html_tag_lines_for_marp(self, content):
        """
        CommonMark treats a line indented with 4+ spaces as an indented code block. Slide
        snippets often align HTML (`<br>`, `<ul>`, `<div>`, …) under column divs, so after a
        markdown math paragraph (column 0) those lines look like code and render as a gray
        <pre> block. Strip leading whitespace only on lines that are clearly HTML tags so
        layout alignment in the source does not break Marp.

        Fenced ``` blocks are unchanged. Slide (Marp) pipeline only.
        """
        import re

        fence_re = re.compile(r"(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$")
        placeholders = []

        def extract_fences(text):
            parts = []
            pos = 0
            for m in fence_re.finditer(text):
                parts.append(text[pos:m.start()])
                i = len(placeholders)
                placeholders.append(m.group(0))
                parts.append(f"<<DEDENTFENCE{i}>>")
                pos = m.end()
            parts.append(text[pos:])
            return "".join(parts)

        text = extract_fences(content)
        out_lines = []
        for line in text.split("\n"):
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            if indent >= 4 and stripped.startswith("<"):
                out_lines.append(stripped)
            else:
                out_lines.append(line)
        text = "\n".join(out_lines)
        for i in range(len(placeholders) - 1, -1, -1):
            text = text.replace(f"<<DEDENTFENCE{i}>>", placeholders[i])
        return text

    def preprocess_math_blocks(self, content):
        """
        Prepare markdown for Marp math ($...$, $$...$$) and optional \\(...\\) (converted to $...$).

        Fenced code blocks (``` ... ```) are left untouched so $ and $$ inside JSON/Python/etc. are not
        treated as math.

        Marp often leaves $$...$$ as literal text inside raw HTML <p>...</p>; unwrap to <div>.
        """
        import re

        # --- Isolate fenced code so $ / $$ inside listings are never math ---
        fence_re = re.compile(r"(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$")
        fence_placeholders = []

        def extract_fences(text):
            out = []
            pos = 0
            for m in fence_re.finditer(text):
                out.append(text[pos:m.start()])
                i = len(fence_placeholders)
                fence_placeholders.append(m.group(0))
                out.append(f"<<MATHFENCE{i}>>")
                pos = m.end()
            out.append(text[pos:])
            return "".join(out)

        content = extract_fences(content)

        # Block math only inside <p> (Marp will not process it there) — allow attributes on <p>
        content = re.sub(
            r"<p\b[^>]*>\s*(\$\$.*?\$\$)\s*</p>",
            r"<div>\1</div>",
            content,
            flags=re.DOTALL,
        )

        block_math_pattern = re.compile(r"(\${2}.*?\${2})", re.DOTALL)
        math_blocks = []

        def math_replacer(match):
            idx = len(math_blocks)
            math_blocks.append(match.group(1))
            return f"__MATH_BLOCK_{idx}__"

        content = block_math_pattern.sub(math_replacer, content)

        # \( ... \) -> $...$ (Pandoc-style; common in authored LaTeX)
        content = re.sub(r"\\\((.*?)\\\)", r"$\1$", content)

        content = re.sub(r"__MATH_BLOCK_\d+__", lambda m: f"\n{m.group(0)}\n", content)
        content = re.sub(r"\n{3,}", "\n\n", content)

        for idx, math_block in enumerate(math_blocks):
            content = content.replace(f"__MATH_BLOCK_{idx}__", math_block)

        # Restore fences (high indices first so tokens like <<MATHFENCE10>> are not corrupted)
        for i in range(len(fence_placeholders) - 1, -1, -1):
            content = content.replace(f"<<MATHFENCE{i}>>", fence_placeholders[i])

        return content

    def lecture_metadata_from_file(self, lecture_file):
        """Parse YAML front matter from a lecture source file."""
        with open(lecture_file, 'r', encoding='utf-8') as f:
            content = f.read()
        front_matter = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if front_matter:
            return yaml.safe_load(front_matter.group(1)) or {}
        return {}

    def process_lecture(self, lecture_file, *, slides_only=False):
        """Process a lecture file to generate all formats (or slides only)."""
        print(f"Processing {lecture_file}...")

        # Get course code from path
        course_code = lecture_file.parent.name

        # Get course metadata
        course_metadata = self.get_course_metadata(course_code)
        lecture_meta = self.lecture_metadata_from_file(lecture_file)

        if lecture_meta.get("instructor_only"):
            print(
                f"[SKIP] Instructor-only source {lecture_file.stem} — "
                "use scripts/big-data-course/build_instructor_notebook.py"
            )
            return

        course_slides_dir = self.assets_dir / "slides" / course_code
        course_slides_dir.mkdir(parents=True, exist_ok=True)

        if slides_only:
            print("[MODE] Slides only - skipping lecture page and notebook")
            if lecture_meta.get('skip_slides'):
                print(f"[SKIP] Slides skipped for {lecture_file.stem} (skip_slides)")
                return
            self.generate_slides(lecture_file, course_slides_dir)
            return

        # Create course-specific directories
        course_lectures_dir = self.lectures_dir / course_code
        course_notebooks_dir = self.assets_dir / "notebooks" / course_code

        for dir_path in [course_lectures_dir, course_slides_dir, course_notebooks_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Read and clean the content first
        with open(lecture_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Protect Python comments in code blocks before any processing
        code_block_pattern = r'```(?:python)?\n(.*?)```'
        def protect_comments(match):
            code = match.group(1)
            # Split into lines and process each line
            lines = code.split('\n')
            protected_lines = []
            for line in lines:
                # Check if line starts with # (after any whitespace)
                if re.match(r'^\s*#', line):
                    # Replace # with a special marker that won't be interpreted as markdown
                    protected_lines.append(re.sub(r'^(\s*)#', r'\1<comment>', line))
                else:
                    protected_lines.append(line)
            return f'```python\n{chr(10).join(protected_lines)}\n```'

        # Replace comments in all code blocks
        content = re.sub(code_block_pattern, protect_comments, content, flags=re.DOTALL)

        # Clean code blocks to remove any markdown/HTML artifacts
        content = self.clean_code_blocks(content)

        # Generate content with course-specific paths
        if not lecture_meta.get('skip_lecture_page'):
            self.generate_rendered_lecture(lecture_file, course_lectures_dir, course_metadata)
        else:
            print(f"[SKIP] Lecture page skipped for {lecture_file.stem} (skip_lecture_page)")
        if not lecture_meta.get('skip_slides'):
            self.generate_slides(lecture_file, course_slides_dir)
        else:
            print(f"[SKIP] Slides skipped for {lecture_file.stem} (skip_slides)")
        if lecture_meta.get('skip_notebook'):
            print(f"[SKIP] Notebook skipped for {lecture_file.stem} (skip_notebook)")
        else:
            self.generate_notebook(lecture_file, course_notebooks_dir, course_metadata)

    def process_talk(self, talk_file):
        """Process a talk source file: generate slides, optional talk page, and update talks.yml."""
        print(f"Processing talk {talk_file}...")
        talk_id = talk_file.stem

        with open(talk_file, 'r', encoding='utf-8') as f:
            content = f.read()
        front_matter = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if front_matter:
            metadata = yaml.safe_load(front_matter.group(1)) or {}
        else:
            metadata = {}

        # Get year from front matter or from existing talks.yml entry
        talks_list = self.load_talks_data()
        existing = next((t for t in talks_list if t.get('talk_id') == talk_id), None)
        year = metadata.get('year') or (existing.get('year') if existing else None)
        if not year:
            raise ValueError(f"Talk {talk_id}: provide 'year' in front matter or add a talks.yml entry with talk_id and year")
        year = int(year)

        # Output dir for slides: assets/slides/<year>/
        course_slides_dir = self.assets_dir / "slides" / str(year)
        course_slides_dir.mkdir(parents=True, exist_ok=True)

        # Generate only slides (no rendered lecture, no notebook)
        self.generate_slides(talk_file, course_slides_dir)

        # Build slides URL: always a single-line absolute URL for talks.yml
        base_url = self.get_site_base_url()
        slides_url = f"{base_url}/assets/slides/{year}/{talk_id}.html".strip()

        # Update or create talks.yml entry (only talk-specific keys)
        talk_entry = {}
        if existing:
            for k in self.TALK_YML_KEYS:
                if k in existing and existing[k] is not None:
                    talk_entry[k] = existing[k]
        talk_entry['talk_id'] = talk_id
        talk_entry['slides'] = slides_url  # always overwrite with generated URL
        if metadata.get('output_page'):
            talk_entry['page'] = f"{base_url}/talks/{year}/{talk_id}/"
        elif existing and existing.get('page'):
            talk_entry['page'] = existing['page']
        for key in self.TALK_YML_KEYS:
            if key in ('slides', 'talk_id'):
                continue
            if metadata.get(key) is not None:
                talk_entry[key] = metadata[key]
        # Default visible to true if unset (same as lectures: front matter controls visibility)
        if 'visible' not in talk_entry:
            talk_entry['visible'] = True
        # Ensure order and only allowed keys for consistent YAML
        ordered = {k: talk_entry[k] for k in self.TALK_YML_KEYS if k in talk_entry and talk_entry[k] is not None}
        if not existing:
            talks_list.append(ordered)
        else:
            idx = next(i for i, t in enumerate(talks_list) if t.get('talk_id') == talk_id)
            talks_list[idx] = ordered
        # Every talk run rewrites _data/talks.yml: merge this talk's entry and refresh slides URL
        self.update_talks_yml(talks_list)
        print(f"[OK] Updated _data/talks.yml for {talk_id}")

        # Optional: generate talk page in content/_talks/
        if metadata.get('output_page'):
            self.talks_dir.mkdir(parents=True, exist_ok=True)
            page_slug = f"{year}-{talk_id}"
            permalink = f"/talks/{year}/{talk_id}/"
            page_metadata = {
                'layout': 'talk',
                'title': ordered.get('title', talk_id),
                'permalink': permalink,
                'talk_id': talk_id,
                'conference': ordered.get('conference', ''),
                'venue': ordered.get('venue', ''),
                'institution': ordered.get('institution', ''),
                'location': ordered.get('location', ''),
                'year': year,
                'month': ordered.get('month', ''),
                'date': ordered.get('date', ''),
                'type': ordered.get('type', ''),
                'status': ordered.get('status', ''),
                'slides': slides_url,
                'description': metadata.get('description', ''),
            }
            body_raw = content[front_matter.end():].lstrip() if front_matter else content
            processed = self.process_includes(body_raw)
            processed = self.process_media(processed)
            body = self.filter_content(processed, 'RENDER')
            body = self.preprocess_math_blocks(body)
            page_content = f"""---
{yaml.dump(page_metadata, default_flow_style=False)}---

<link rel="stylesheet" href="/assets/css/slides.css">
<div class="lecture-resources">
  <p><a href="{slides_url}" target="_blank" rel="noopener noreferrer">[View Slides]</a></p>
</div>

{body}
"""
            output_file = self.talks_dir / f"{page_slug}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_content)
            print(f"[OK] Wrote talk page {output_file}")

    def clean_code_blocks(self, content):
        """Clean code blocks to remove markdown/HTML artifacts."""
        # Pattern to match code blocks, including those inside HTML elements
        code_block_pattern = r'```(?:python)?\n(.*?)```'

        def clean_code(match):
            code = match.group(1)
            # Remove any HTML tags while preserving their content
            code = re.sub(r'<[^>]+>', '', code)
            # Remove any markdown syntax
            code = re.sub(r'^---$', '', code, flags=re.MULTILINE)
            # Remove empty lines at start and end
            code = code.strip()

            # Add line numbers and proper formatting
            lines = code.split('\n')
            numbered_lines = []
            for i, line in enumerate(lines, 1):
                # Add proper indentation and line number
                numbered_lines.append(f"{i:3d} | {line}")
            code = '\n'.join(numbered_lines)

            return f'```python\n{code}\n```'

        # First, temporarily replace HTML elements containing code blocks
        html_code_blocks = []
        def replace_html_code(match):
            html_content = match.group(0)
            # Find all code blocks within this HTML element
            code_matches = list(re.finditer(code_block_pattern, html_content, re.DOTALL))
            if code_matches:
                # Replace each code block with a placeholder
                for i, code_match in enumerate(code_matches):
                    placeholder = f'__CODE_BLOCK_{len(html_code_blocks)}_{i}__'
                    html_code_blocks.append((placeholder, code_match.group(0)))
                    html_content = html_content.replace(code_match.group(0), placeholder)
            return html_content

        # Find HTML elements that might contain code blocks
        html_pattern = r'<[^>]+>.*?```.*?```.*?</[^>]+>'
        content = re.sub(html_pattern, replace_html_code, content, flags=re.DOTALL)

        # Now process all code blocks in the content
        processed_content = re.sub(code_block_pattern, clean_code, content, flags=re.DOTALL)

        # Restore the code blocks from HTML elements
        for placeholder, code_block in html_code_blocks:
            processed_content = processed_content.replace(placeholder, clean_code(re.match(code_block_pattern, code_block)))

        # Add custom styling for code blocks
        style_block = """
<style>
/* Code block container */
pre {
  background-color: var(--code-bg);
  border: 1px solid var(--code-border);
  border-radius: 6px;
  padding: 16px;
  margin: 0;
  width: 100%;
  font-size: 0.9em;
  line-height: 1.45;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-width: 100%;
  box-sizing: border-box;
  position: relative;
  overflow-x: auto;
}

/* Code content */
code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.9em;
  line-height: 1.45;
  color: var(--code-text);
  max-width: 100%;
  display: block;
  tab-size: 4;
}

/* Line numbers */
code::before {
  content: attr(data-line-numbers);
  position: absolute;
  left: 0;
  padding-right: 1em;
  color: #666;
  border-right: 1px solid #ddd;
  user-select: none;
}

/* Syntax highlighting for light theme */
.hljs-keyword,
.hljs-selector-tag,
.hljs-title,
.hljs-section {
  color: #0000FF;  /* Python blue for keywords */
}

.hljs-string,
.hljs-doctag {
  color: #008000;  /* Python green for strings */
}

.hljs-number,
.hljs-literal {
  color: #0000CD;  /* Python medium blue for numbers */
}

.hljs-comment {
  color: #808080;  /* Python gray for comments */
}

.hljs-function,
.hljs-class .hljs-title {
  color: #000000;  /* Python black for function names */
}

/* Syntax highlighting for dark theme */
html[data-theme='dark'] .hljs-keyword,
html[data-theme='dark'] .hljs-selector-tag,
html[data-theme='dark'] .hljs-title,
html[data-theme='dark'] .hljs-section {
  color: #569CD6;  /* Light blue for keywords */
}

html[data-theme='dark'] .hljs-string,
html[data-theme='dark'] .hljs-doctag {
  color: #6A9955;  /* Light green for strings */
}

html[data-theme='dark'] .hljs-number,
html[data-theme='dark'] .hljs-literal {
  color: #B5CEA8;  /* Light blue-green for numbers */
}

html[data-theme='dark'] .hljs-comment {
  color: #6A9955;  /* Light gray-green for comments */
}

html[data-theme='dark'] .hljs-function,
html[data-theme='dark'] .hljs-class .hljs-title {
  color: #DCDCAA;  /* Light yellow for function names */
}

/* Code block hover effect */
pre:hover {
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
}

/* Copy button */
pre::after {
  content: '📋';
  position: absolute;
  top: 5px;
  right: 5px;
  padding: 5px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s ease;
}

pre:hover::after {
  opacity: 1;
}

/* Code block focus styles */
pre:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--accent-color);
}

/* Ensure code blocks are properly contained */
.slide-content pre {
  max-height: 100%;
  overflow-y: auto;
}

/* Improve code readability */
code {
  letter-spacing: 0.3px;
}

/* Add subtle background to line numbers */
code::before {
  background-color: rgba(0,0,0,0.03);
  padding: 0.5em 1em;
  margin: -0.5em 0;
}

html[data-theme='dark'] code::before {
  background-color: rgba(255,255,255,0.05);
}
</style>
"""
        # Add the style block to the content
        processed_content = style_block + processed_content

        return processed_content

    def generate_rendered_lecture(self, lecture_file, output_dir, course_metadata):
        """Generate the rendered lecture file with proper metadata and content."""
        # Read source content
        with open(lecture_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract front matter from source
        front_matter = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if front_matter:
            lecture_metadata = yaml.safe_load(front_matter.group(1))
            content = content[front_matter.end():]
        else:
            lecture_metadata = {}

        # Merge course and lecture metadata, preserving all fields
        metadata = lecture_metadata.copy()
        metadata.update({
            'layout': 'lecture',
            'lecture_code': lecture_file.stem,
            'course_code': course_metadata.get('course_code', ''),
            'permalink': f"/teaching/{course_metadata.get('course_code', '')}/{lecture_file.stem}/"
        })

        # Process includes and media first, then filter for RENDER tags
        processed_content = self.process_includes(content)
        processed_content = self.process_media(processed_content)
        filtered_content = self.filter_content(processed_content, 'RENDER')
        # Preprocess math blocks for correct rendering
        filtered_content = self.preprocess_math_blocks(filtered_content)

        resources_html = self._lecture_resources_html(
            lecture_file, course_metadata, lecture_metadata
        )
        # Create rendered content with metadata and resources
        rendered_content = f"""---
{yaml.dump(metadata, default_flow_style=False)}---

<link rel=\"stylesheet\" href=\"/assets/css/slides.css\">
<link rel=\"stylesheet\" href=\"/assets/css/lecture-article.css\">
{resources_html}

{filtered_content}
"""

        # Save rendered lecture
        output_file = output_dir / lecture_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

    def _lecture_resources_html(self, lecture_file, course_metadata, lecture_metadata):
        """Top-of-page links: slides (optional), Colab(s), course home."""
        course_code = course_metadata.get('course_code', '')
        stem = lecture_file.stem
        colab_base = (
            "https://colab.research.google.com/github/cabrerac/cabrerac.github.io"
            f"/blob/gh-pages/assets/notebooks/{course_code}"
        )
        links = []
        if not lecture_metadata.get('skip_slides'):
            links.append(
                f'<a href="/assets/slides/{course_code}/{stem}.html" target="_blank">'
                "HTML slides</a>"
            )
        if not lecture_metadata.get('skip_notebook'):
            links.append(
                f'<a href="{colab_base}/{stem}.ipynb" target="_blank">'
                "Notebook - Individual</a>"
            )
        group_nb = lecture_metadata.get('group_notebook')
        if group_nb and not lecture_metadata.get('skip_notebook'):
            links.append(
                f'<a href="{colab_base}/{group_nb}.ipynb" target="_blank">'
                "Notebook - Group</a>"
            )
        links.append(f'<a href="/teaching/{course_code}/">Back to course</a>')
        return (
            '<div class="lecture-resources">\n  <p>\n    '
            + " &nbsp;|&nbsp; ".join(links)
            + "\n  </p>\n</div>"
        )

    def generate_slides(self, lecture_file, output_dir):
        """Generate Marp slides from lecture content."""
        lecture_content = self.read_snippet(lecture_file)

        # Process includes first
        processed_content = self.process_includes(lecture_content)
        processed_content = self.process_media(processed_content)

        # Filter content for slides
        filtered_content = self.filter_content(processed_content, 'SLIDES')
        # Let authors use <p>...</p> with $...$; Marp ignores math inside raw HTML unless we unwrap
        filtered_content = self.unwrap_html_paragraphs_for_marp_math(filtered_content)
        # Aligning HTML under columns uses 4+ space indent; CommonMark would treat that as a code block
        filtered_content = self.dedent_indented_html_tag_lines_for_marp(filtered_content)
        filtered_content = self.preprocess_math_blocks(filtered_content)

        slide_blocks = self.split_filtered_content_into_slide_blocks(filtered_content)

        slides = []
        pdf_slides = []  # Store slides marked for PDF separately

        for block in slide_blocks:
            block_lines = block.strip().split('\n')
            if not block_lines:
                continue
            first_line = block_lines[0].strip()

            # Check if this slide should be included in PDF
            include_in_pdf = self.check_pdf_slide(block)

            # Title slide (# ...)
            if first_line.startswith('# '):
                title = first_line[2:].strip()
                # Everything after the title is ignored for title slide
                slide = f'''<!-- _class: lead -->
<div class="slide-content" style="display: flex; align-items: center; height: 100%; justify-content: flex-start;">
<h1 style="margin: 0; padding: 0; text-align: left;">{title}</h1>
</div>'''
                slides.append(slide)
                # Always include title slide in PDF
                pdf_slides.append(slide)
            # Section slide (## ...)
            elif first_line.startswith('## '):
                heading = first_line
                content = '\n'.join(block_lines[1:])
                # Replace all ### ... with a styled subtitle inside slide-content
                content = re.sub(r'^### (.*)$', r'<h3 style="margin-top:0;margin-bottom:0.5em;text-align:left;">\1</h3>', content, flags=re.MULTILINE)
                slide = f'{heading}\n\n<div class="slide-content">\n{content}\n</div>'
                slides.append(slide)
                if include_in_pdf:
                    pdf_slides.append(slide)
            else:
                # Fallback: treat as content slide
                content = '\n'.join(block_lines)
                content = re.sub(r'^### (.*)$', r'<h3 style="margin-top:0;margin-bottom:0.5em;text-align:left;">\1</h3>', content, flags=re.MULTILINE)
                slide = f'<div class="slide-content">\n{content}\n</div>'
                slides.append(slide)
                if include_in_pdf:
                    pdf_slides.append(slide)

        # Join slides with Marp slide separator
        slides_content = '\n\n---\n\n'.join(slides)
        pdf_slides_content = '\n\n---\n\n'.join(pdf_slides)

        # Extract front matter
        front_matter = re.match(r'^---\n(.*?)\n---', lecture_content, re.DOTALL)
        if front_matter:
            metadata = yaml.safe_load(front_matter.group(1))
        else:
            metadata = {
                'title': lecture_file.stem,
                'session': '1',
                'description': 'Lecture'
            }

        # Header: for talks use venue, for lectures use session
        slide_header = (f"{metadata.get('venue', '')} - {metadata.get('title', '')}"
                        if metadata.get('venue') else
                        f"Session {metadata.get('session', '1')} - {metadata.get('title', '')}")
        show_slide_counter = metadata.get('show_slide_counter', True)
        counter_css = """section::before {
    font-size: 0.6em;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    position: absolute;
    text-align: right;
    bottom: 1em;
    right: 1em;
    color: var(--secondary-color);
  }""" if show_slide_counter else """section::before {
    display: none !important;
  }"""
        # Template for slides (removing duplicated lead sections)
        marp_template = f"""---
marp: true
theme: default
math: mathjax
paginate: true
header: "{slide_header}"
footer: ""
style: |
  :root {{
    --primary-color: #224466;
    --secondary-color: #0e73b8;
    --accent-color: #0e73b8;
    --text-color: #224466;
    --background-color: #ffffff;
    --progress-color: #0e73b8;
    --code-bg: #f6f8fa;
    --code-text: #24292e;
    --code-border: #e1e4e8;
  }}

  html[data-theme='dark'] {{
    --primary-color: #ffffff;
    --secondary-color: #0e73b8;
    --accent-color: #0e73b8;
    --text-color: #ffffff;
    --background-color: #0d1117;
    --progress-color: #0e73b8;
    --code-bg: #161b22;
    --code-text: #c9d1d9;
    --code-border: #30363d;
  }}

  section:not(.lead) {{
    position: relative;
  }}

  section:not(.lead) > h2 {{
    text-align: left;
    font-size: 1.25em;
    color: var(--text-color);
    margin: 1em 0;
    position: absolute;
    top: 1rem;
    left: 1rem;
    width: calc(100% - 2rem);
  }}

  section:not(.lead) .slide-content {{
    position: absolute;
    top: calc(1.75rem + 1.25em + 1em);
    left: 0.5rem;
    width: calc(100% - 1rem);
    height: calc(100% - (2rem + 1.5em + 1em + 1rem));
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    overflow: hidden;
  }}

  /* Timeline specific styles */
  .timeline-container {{
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }}

  .timeline-container svg {{
    width: 100%;
    height: 100%;
    max-height: 100%;
    margin: 0 auto;
  }}

  .timeline-container path {{
    stroke: var(--secondary-color);
    stroke-width: 3;
    fill: none;
    stroke-dasharray: 5,5;
  }}

  .timeline-container circle {{
    fill: var(--secondary-color);
    r: 6;
  }}

  .timeline-container text {{
    fill: var(--text-color);
    font-size: 12px;
    font-family: Arial, sans-serif;
  }}

  .timeline-container image {{
    fill: var(--secondary-color);
  }}

  .timeline-container .event-description {{
    position: absolute;
    top: 30px;
    left: 30px;
    width: 200px;
    color: var(--text-color);
  }}

  .timeline-container .event-description p {{
    font-size: 14px;
    margin: 5px 0;
  }}

  /* Ensure all direct children of slide-content respect its boundaries */
  section:not(.lead) .slide-content > * {{
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
  }}

  /* Ensure rows and columns respect their container's boundaries */
  .rows, .columns {{
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
  }}

  .row, .column {{
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
  }}

  /* Ensure images scale properly */
  .slide-content img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    width: auto;
    height: auto;
  }}

  /* Ensure code blocks fit without scrolling */
  .slide-content pre {{
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
    font-size: 0.8em;
    line-height: 1.2;
    padding: 0.5em;
  }}

  .slide-content div {{
    color: var(--text-color);
  }}

  /* Ensure text content fits */
  .slide-content p {{
    margin: 0;
    padding: 0.2em;
    font-size: 0.9em;
    line-height: 1.2;
  }}

  /* MathJax (Marp math: mathjax) — match slide text colour */
  section .MathJax,
  section mjx-container {{
    color: var(--text-color) !important;
  }}

  /* Scale down content if it would overflow */
  .slide-content {{
    transform-origin: top left;
  }}

  .slide-content.overflow {{
    transform: scale(0.95);
  }}

  /* Main title (h1) styling */
  section:not(.lead) .slide-content > h1 {{
    text-align: left;
    font-size: 1.5em;
    font-weight: bold;
    margin: 0;
    padding: 0;
    color: var(--text-color);
    width: 100%;
  }}

  /* Content styling */
  section:not(.lead) .slide-content > *:not(h1):not(h2) {{
    margin: 0;
    width: 100%;
  }}

  /* Code block styling */
  pre {{
    background-color: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 6px;
    padding: 16px;
    margin: 0;
    width: 100%;
    font-size: 0.9em;
    line-height: 1.45;
    white-space: pre-wrap;
    word-wrap: break-word;
    max-width: 100%;
    box-sizing: border-box;
  }}

  code {{
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.9em;
    line-height: 1.45;
    color: var(--code-text);
    max-width: 100%;
    display: block;
  }}

  /* Syntax highlighting for light theme */
  .hljs-keyword,
  .hljs-selector-tag,
  .hljs-title,
  .hljs-section {{
    color: #0000FF;  /* Python blue for keywords */
  }}

  .hljs-string,
  .hljs-doctag {{
    color: #008000;  /* Python green for strings */
  }}

  .hljs-number,
  .hljs-literal {{
    color: #0000CD;  /* Python medium blue for numbers */
  }}

  .hljs-comment {{
    color: #808080;  /* Python gray for comments */
  }}

  .hljs-function,
  .hljs-class .hljs-title {{
    color: #000000;  /* Python black for function names */
  }}

  /* Syntax highlighting for dark theme */
  html[data-theme='dark'] .hljs-keyword,
  html[data-theme='dark'] .hljs-selector-tag,
  html[data-theme='dark'] .hljs-title,
  html[data-theme='dark'] .hljs-section {{
    color: #569CD6;  /* Light blue for keywords */
  }}

  html[data-theme='dark'] .hljs-string,
  html[data-theme='dark'] .hljs-doctag {{
    color: #6A9955;  /* Light green for strings */
  }}

  html[data-theme='dark'] .hljs-number,
  html[data-theme='dark'] .hljs-literal {{
    color: #B5CEA8;  /* Light blue-green for numbers */
  }}

  html[data-theme='dark'] .hljs-comment {{
    color: #6A9955;  /* Light gray-green for comments */
  }}

  html[data-theme='dark'] .hljs-function,
  html[data-theme='dark'] .hljs-class .hljs-title {{
    color: #DCDCAA;  /* Light yellow for function names */
  }}

  .columns {{
    display: flex;
    flex-wrap: nowrap;
    gap: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }}

  .rows {{
    display: flex;
    flex-direction: column;
    gap: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }}

  /* Default equal distribution for columns */
  .columns > .column {{
    flex: 1;
    min-width: 0;
    min-height: 0;
    display: flex;
    flex-direction: column;
    gap: 0;
    padding: 0;
    overflow: hidden;
    color: var(--text-color);
  }}

  /* Default equal distribution for rows */
  .rows > .row {{
    flex: 1;
    min-width: 0;
    min-height: 0;
    display: flex;
    flex-direction: column;
    gap: 0;
    padding: 0;
    overflow: hidden;
    color: var(--text-color);
  }}

  /* Specific column widths */
  .columns > .column[style*="width:"] {{
    flex: 0 0 auto;
    width: var(--column-width);
  }}

  /* Specific row heights */
  .rows > .row[style*="height:"] {{
    flex: 0 0 auto;
    height: var(--row-height);
  }}

  /* Vertical positioning for column and row content */
  .column.vertical-top, .row.vertical-top {{
    justify-content: flex-start;
  }}

  .column.vertical-middle, .row.vertical-middle {{
    justify-content: center;
  }}

  .column.vertical-bottom, .row.vertical-bottom {{
    justify-content: flex-end;
  }}

  /* Specific styles for text alignment */
  .column.text-center, .row.text-center {{
    text-align: center;
  }}

  .column.text-left, .row.text-left {{
    text-align: left;
  }}

  .column.text-right, .row.text-right {{
    text-align: right;
  }}

  /* Content styling */
  .column p, .row p {{
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--text-color);
  }}

  .column strong, .row strong {{
    color: var(--text-color);
  }}

  .column em, .row em {{
    color: var(--text-color);
  }}

  /* Image scaling styles */
  .column img, .row img {{
    object-fit: contain;
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    display: block;
    margin: 0 auto;
  }}

  /* Specific height with auto width */
  .column img[style*="height:"], .row img[style*="height:"] {{
    width: auto !important;
    max-width: 100%;
  }}

  /* Specific width with auto height */
  .column img[style*="width:"], .row img[style*="width:"] {{
    height: auto !important;
    max-height: 100%;
  }}

  /* Fix for inline styles */
  .column img[style*="width:"][style*="height:"],
  .row img[style*="width:"][style*="height:"] {{
    object-fit: contain;
    max-width: 100%;
    max-height: 100%;
  }}

  /* Ensure containers properly contain their content */
  .column > *, .row > * {{
    max-width: 100%;
    overflow: hidden;
  }}

  .footnote {{
    font-size: 0.6em;
    color: var(--accent-color);
    margin: 0;
    text-align: center;
    font-style: italic;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Ensure links use accent color */
  .column a, .row a {{
    color: var(--accent-color);
    text-decoration: none;
  }}

  .column a:hover, .row a:hover {{
    text-decoration: underline;
  }}

  /* Override any specific link colors in dark mode */
  html[data-theme='dark'] .column a,
  html[data-theme='dark'] .row a {{
    color: var(--accent-color) !important;
  }}

  /* Ensure email links maintain accent color */
  html[data-theme='dark'] .column a[href^="mailto:"],
  html[data-theme='dark'] .row a[href^="mailto:"] {{
    color: var(--accent-color) !important;
  }}

  html[data-theme='dark'] section .slide-content img.external-svg {{
        background-color: #f6f8fa !important;
  }}

  html[data-theme='dark'] section .slide-content div {{
    color: #FFFFFF !important;
  }}

  {counter_css}

  section::after {{
    display: none !important;
  }}

  header {{
    color: var(--text-color);
    font-size: 20px;
    padding: 10px;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--accent-color);
    z-index: 100;
  }}

  section.lead h1 {{
    margin-bottom: 10px;
  }}

  section.lead p {{
    font-size: 24px;
    margin: 5px 0;
    line-height: 1.2;
  }}

  section.lead header {{
    display: none;
  }}

  section.lead.last-slide {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }}

  section.lead.last-slide h1 {{
    margin-bottom: 20px;
  }}

  section.lead.last-slide p {{
    margin: 10px 0;
  }}

  /* Table specific styles */
  .table {{
    display: inline-block;
    text-align: left;
    background-color: white !important;
    padding: 10px;
    border-radius: 5px;
    margin: 0 auto;
  }}

  .table th,
  .table td {{
    color: #000000 !important;
  }}

  /* Ensure table text stays black in dark mode */
  html[data-theme='dark'] .table th,
  html[data-theme='dark'] .table td {{
    color: #000000 !important;
  }}

  /* Ensure table background stays white in dark mode */
  html[data-theme='dark'] .table {{
    background-color: white !important;
  }}

  /* Ensure highlighted row maintains its color in dark mode */
  html[data-theme='dark'] .table tr[style*="background-color: #e6ffe6"] {{
    background-color: #e6ffe6 !important;
  }}

  /* Ensure table container is centered */
  .column.text-center .table {{
    margin: 0 auto;
  }}

  /* Ensure list elements match paragraph text size */
  .slide-content ul li,
  .slide-content ol li {{
    font-size: 0.9em;
    line-height: 1.2;
    margin: 0;
    padding: 0.2em;
  }}

  /* Ensure list elements maintain text color in dark mode */
  html[data-theme='dark'] .slide-content ul li,
  html[data-theme='dark'] .slide-content ol li {{
    color: var(--text-color) !important;
  }}
---"""

        # Internal talks: title and thanks slides show only author name (no affiliation)
        # Multi-line titles: separate lines with YAML newlines/title_slide: | block or the in-line marker @NL@ (never split on ':').
        is_internal = metadata.get('type') == 'internal'
        display_title = metadata.get('title_slide', metadata.get('title', ''))
        if is_internal:
            td = display_title.strip() if isinstance(display_title, str) else ''
            raw_parts = []
            if td:
                if '@NL@' in td:
                    for seg in td.split('@NL@'):
                        raw_parts.extend(
                            [p.strip() for p in re.split(r'\r?\n', seg) if p.strip()]
                        )
                else:
                    raw_parts = [p.strip() for p in re.split(r'\r?\n', td) if p.strip()]
            author_raw = metadata.get('author') or ''
            author_esc = escape(author_raw)
            if len(raw_parts) >= 2:
                h1_inner = '<br>'.join(escape(p) for p in raw_parts)
            elif raw_parts:
                h1_inner = escape(raw_parts[0])
            else:
                h1_inner = ''
            title_block = f"""<!-- _class: lead -->
<div class="slide-content" style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:1rem;width:100%;min-height:100%;box-sizing:border-box;">
<h1 style="margin: 0; padding: 0; text-align: left;">{h1_inner}</h1>
<p style="margin: 0; color: var(--text-color);"><b>{author_esc}</b></p>
</div>"""
            thanks_block = """<!-- _class: lead last-slide -->
# Many Thanks!"""
        else:
            title_block = f"""<!-- _class: lead -->
# {display_title}
<p style="color: var(--text-color);"><b>{metadata.get('author', '')}</b></p>
<p style="color: var(--text-color);">{metadata.get('position', '')}</p>
<p style="color: var(--text-color);">{metadata.get('department', '')}</p>
<p style="color: var(--text-color);">{metadata.get('institution', '')}</p>
<p style="color: var(--accent-color);"><a href="mailto:{metadata.get('email', '')}" style="color: var(--accent-color);">{metadata.get('email', '')}</a></p>"""
            thanks_extended = metadata.get('thanks_slides_qr') or metadata.get('thanks_extended')
            email = metadata.get('email', '') or ''
            website_url = (metadata.get('thanks_website_url') or '').strip()
            if thanks_extended:
                qr_target = (metadata.get('thanks_qr_target_url') or '').strip()
                if not qr_target:
                    qr_target = self.resolve_public_slides_url(metadata, lecture_file.stem) or ''
                if not qr_target:
                    print(
                        "Warning: thanks_slides_qr is set but no slides URL could be built; "
                        "set thanks_qr_target_url or ensure year and talk_id (or file stem) are in front matter."
                    )
                qr_src = ''
                if qr_target:
                    qr_src = (
                        "https://api.qrserver.com/v1/create-qr-code/?size=240x240&data="
                        + quote(qr_target, safe='')
                    )
                esc_website_href = escape(website_url, quote=True) if website_url else ''
                esc_website_text = escape(website_url) if website_url else ''
                esc_email_href = escape(email, quote=True)
                esc_email_text = escape(email)
                qr_img = ''
                if qr_src:
                    esc_qr_src = escape(qr_src, quote=True)
                    qr_img = (
                        f'<p style="margin:0;">'
                        f'<img src="{esc_qr_src}" alt="QR code: link to slides" '
                        f'style="width:220px;height:220px;object-fit:contain;">'
                        f'</p>'
                    )
                website_line = ''
                if website_url:
                    website_line = (
                        f'<p style="margin:0;padding:0.2em;">'
                        f'<a href="{esc_website_href}" style="color:var(--accent-color);">{esc_website_text}</a>'
                        f'</p>'
                    )
                thanks_block = f"""<!-- _class: lead last-slide -->
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;gap:0.55rem;padding:0.75rem;">
{qr_img}
<h1 style="margin:0;color:var(--text-color);">Many Thanks!</h1>
{website_line}
<p style="margin:0;padding:0.2em;"><a href="mailto:{esc_email_href}" style="color:var(--accent-color);">{esc_email_text}</a></p>
</div>"""
            else:
                thanks_block = f"""<!-- _class: lead last-slide -->
# Many Thanks!
<p style="color: var(--accent-color);"><a href="mailto:{metadata.get('email', '')}" style="color: var(--accent-color);">{metadata.get('email', '')}</a></p>"""

        # Create Marp slides for HTML (all slides)
        html_content = f"""
{title_block}

---

{slides_content}

---

{thanks_block}
"""

        # Create Marp slides for PDF (only marked slides)
        pdf_content = f"""
{title_block}

---

{pdf_slides_content}

---

{thanks_block}
"""

        # Save markdown slides for HTML
        html_file = output_dir / f"{lecture_file.stem}.html.md"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(marp_template + html_content + """
<!-- _script: true -->
<!-- This script will only execute in HTML slides -->
<script>
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('section').forEach((section, i, all) => {
      const bar = document.createElement('div');
      bar.style.position = 'absolute';
      bar.style.bottom = '0';
      bar.style.left = '0';
      bar.style.height = '4px';
      bar.style.backgroundColor = '#0E73B8';
      bar.style.width = `${((i + 1) / all.length) * 100}%`;
      bar.style.zIndex = '9';
      section.appendChild(bar);
    });
  });
</script>

<!-- _script: true -->
<script>
  // Add theme toggle button to body once slides load
  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.createElement("div");
    toggle.id = "theme-toggle";
    toggle.innerHTML = "🌔";
    document.body.appendChild(toggle);

    const style = document.createElement("style");
    style.textContent = `
      #theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: var(--accent-color);
        color: var(--background-color);
        padding: 0.5em;
        width: 1.5em;
        height: 1.5em;
        border-radius: 50%;
        font-size: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 9999;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        user-select: none;
        transition: transform 0.3s ease;
      }

      #theme-toggle:hover {
        transform: scale(1.1);
      }

      html[data-theme='dark'] {
        --primary-color: #FFFFFF;
        --secondary-color: #0E73B8;
        --accent-color: #0E73B8;
        --text-color: #FFFFFF;
        --background-color: #1E1E1E;
        --progress-color: #0E73B8;
      }

      html[data-theme='light'] {
        --primary-color: #00244A;
        --secondary-color: #0E73B8;
        --accent-color: #0E73B8;
        --text-color: #00244A;
        --background-color: #FFFFFF;
        --progress-color: #0E73B8;
      }

      html[data-theme='dark'] section {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
      }

      html[data-theme='dark'] h1,
      html[data-theme='dark'] h2,
      html[data-theme='dark'] h3,
      html[data-theme='dark'] h4,
      html[data-theme='dark'] h5,
      html[data-theme='dark'] h6 {
        color: #FFFFFF !important;
      }

      html[data-theme='dark'] a {
        color: #0E73B8 !important;
      }

      html[data-theme='dark'] body,
      html[data-theme='dark'] .marpit {
        background-color: #1E1E1E !important;
      }

      html[data-theme='dark'] header {
        color: #FFFFFF !important;
      }

      /* Explicit dark mode styles for paragraphs and their children */
      html[data-theme='dark'] section p,
      html[data-theme='dark'] section .slide-content div,
      html[data-theme='dark'] section ul,
      html[data-theme='dark'] section ol,
      html[data-theme='dark'] section p *,
      html[data-theme='dark'] section .column p,
      html[data-theme='dark'] section .column p *,
      html[data-theme='dark'] section .row p,
      html[data-theme='dark'] section .row p *,
      html[data-theme='dark'] section p strong,
      html[data-theme='dark'] section p em,
      html[data-theme='dark'] section .column p strong,
      html[data-theme='dark'] section .column p em,
      html[data-theme='dark'] section .row p strong,
      html[data-theme='dark'] section .row p em {
        color: #FFFFFF !important;
      }

      html[data-theme='dark'] section .pre {
        background-color: #2A2A2A !important;
      }

      html[data-theme='dark'] section .slide-content img {
        background-color: #1e1e1e !important;
      }

      html[data-theme='dark'] section .timeline-container circle {
        fill: #0E73B8 !important;
      }
      html[data-theme='dark'] section .timeline-container image {
        fill: #0E73B8 !important;
      }

      /* Link styling */
      a {
        color: var(--accent-color);
        text-decoration: none;
      }

      a:hover {
        text-decoration: underline;
      }

      /* Ensure links maintain accent color in dark mode */
      html[data-theme='dark'] a {
        color: var(--accent-color) !important;
      }

      /* Override any specific link colors */
      html[data-theme='dark'] section p a,
      html[data-theme='dark'] section .column p a,
      html[data-theme='dark'] section .row p a {
        color: var(--accent-color) !important;
      }

      html[data-theme='dark'] section .slide-content img.external-svg {
        background-color: #f6f8fa !important;
      }

      /* Ensure email links maintain accent color */
      html[data-theme='dark'] section p a[href^="mailto:"] {
        color: var(--accent-color) !important;
      }
    `;
    document.head.appendChild(style);

    function setTheme(theme) {
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
      toggle.innerHTML = theme === "dark" ? "🌔" : "🌒";

      // Force update paragraph colors
      if (theme === "dark") {
        document.querySelectorAll('section p, section p *, section .column p, section .column p *, section .row p, section .row p *').forEach(el => {
          el.style.color = '#FFFFFF !important';
        });
      }
    }

    toggle.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      setTheme(current === "dark" ? "light" : "dark");
    });

    const stored = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (stored) {
      setTheme(stored);
    } else {
      setTheme(prefersDark ? "dark" : "light");
    }
  });
</script>
""")

        # Save markdown slides for PDF
        #pdf_file = output_dir / f"{lecture_file.stem}.pdf.md"
        #with open(pdf_file, 'w', encoding='utf-8') as f:
        #    f.write(marp_template + pdf_content)

        # Generate PDF and HTML slides using Marp CLI
        try:
            # Try to find marp in common locations, with your specific path first
            marp_paths = [
                os.path.join(os.environ.get('APPDATA', ''), 'npm', 'marp.cmd'),  # Your specific path
                'marp.cmd',  # Windows global install
                os.path.join(os.environ.get('ProgramFiles', ''), 'nodejs', 'marp.cmd'),
                os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'nodejs', 'marp.cmd'),
                os.path.join(os.path.expanduser('~'), '.npm-global', 'bin', 'marp.cmd'),
            ]

            marp_cmd = None
            for path in marp_paths:
                if os.path.exists(path):
                    print(f"Found Marp at: {path}")
                    marp_cmd = path
                    break
                elif shutil.which(path):
                    print(f"Found Marp in PATH: {path}")
                    marp_cmd = path
                    break

            if not marp_cmd:
                # Try using npx as a fallback
                try:
                    subprocess.run(['npx', '--version'], check=True, capture_output=True)
                    marp_cmd = ['npx', '@marp-team/marp-cli']
                    print("Using npx to run Marp")
                except:
                    raise FileNotFoundError("Marp CLI not found in any common locations")

            # Generate PDF from PDF-specific file
            """if isinstance(marp_cmd, list):
                pdf_cmd = marp_cmd + [
                    str(pdf_file),
                    '--pdf',
                    '--allow-local-files',
                    '--theme-set', str(self.assets_dir / "css/dark-theme.css"),
                    '--html',
                    '-o', str(output_dir / f"{lecture_file.stem}.pdf")
                ]
            else:
                pdf_cmd = [
                    marp_cmd,
                    str(pdf_file),
                    '--pdf',
                    '--allow-local-files',
                    '--theme-set', str(self.assets_dir / "css/dark-theme.css"),
                    '--html',
                    '-o', str(output_dir / f"{lecture_file.stem}.pdf")
                ]

            print(f"Running command: {' '.join(pdf_cmd)}")
            subprocess.run(pdf_cmd, check=True)"""

            # Generate HTML from the HTML-specific file (--no-stdin so Marp reads from file, not stdin)
            if isinstance(marp_cmd, list):
                html_cmd = marp_cmd + [
                    '--no-stdin',
                    str(html_file),
                    '--html',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.html")
                ]
            else:
                html_cmd = [
                    marp_cmd,
                    '--no-stdin',
                    str(html_file),
                    '--html',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.html")
                ]

            # On Windows, marp.cmd invokes node; ensure Node.js is on PATH in the subprocess
            run_env = None
            if os.name == 'nt':
                node_dirs = [
                    os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'nodejs'),
                    os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'nodejs'),
                    os.path.join(os.environ.get('APPDATA', ''), 'npm'),
                    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'nodejs'),
                ]
                extra = os.pathsep.join(d for d in node_dirs if d and os.path.isdir(d))
                if extra:
                    run_env = {**os.environ, 'PATH': extra + os.pathsep + os.environ.get('PATH', '')}

            print(f"Running command: {' '.join(html_cmd)}")
            subprocess.run(html_cmd, check=True, env=run_env)

            # Remove the temporary files
            os.remove(html_file)
            #os.remove(pdf_file)

            print(f"[OK] Successfully generated slides for {lecture_file.stem}")
        except subprocess.CalledProcessError as e:
            out = (e.output or e.stderr or b'').decode(errors='replace')
            print(f"Error: Failed to generate slides: {e}")
            if out:
                print(f"Command output: {out}")
            if 'node' in out.lower() or 'not recognized' in out.lower():
                print("Marp CLI requires Node.js. Ensure Node.js is installed and on your PATH:")
                print("  https://nodejs.org/")
            print("Then install Marp: npm install -g @marp-team/marp-cli")
            raise
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please install Marp CLI using one of these methods:")
            print("1. npm install -g @marp-team/marp-cli")
            print("2. yarn global add @marp-team/marp-cli")
            print("3. npx @marp-team/marp-cli")
            print("\nIf Marp is already installed, try:")
            print("1. Restart your terminal")
            print("2. Check if the installation path is in your system's PATH")
            print("3. Try running 'marp --version' to verify the installation")
            raise

    _NOTEBOOK_FENCE_RE = re.compile(
        r"^```python\s*\n(.*?)^```\s*$",
        re.MULTILINE | re.DOTALL,
    )

    def _split_markdown_sections(self, markdown: str) -> list[str]:
        """Split markdown prose into cells on blank-line boundaries."""
        return [section.strip() for section in markdown.split("\n\n") if section.strip()]

    def _iter_notebook_blocks(self, content: str):
        """
        Yield ('markdown', text) or ('code', text) in document order.

        Fenced ```python blocks must stay intact (blank lines inside code are common).
        The previous split-on-\\n\\n approach broke code blocks into markdown fragments.
        """
        pos = 0
        for match in self._NOTEBOOK_FENCE_RE.finditer(content):
            md = content[pos : match.start()].strip()
            if md:
                for section in self._split_markdown_sections(md):
                    yield ("markdown", section)
            code = match.group(1)
            if code.endswith("\n"):
                code = code[:-1]
            yield ("code", code)
            pos = match.end()
        tail = content[pos:].strip()
        if tail:
            for section in self._split_markdown_sections(tail):
                yield ("markdown", section)

    def generate_notebook(self, lecture_file, output_dir, course_metadata):
        """Generate Jupyter notebook from lecture content."""
        print(f"Generating notebook for {lecture_file}")

        lecture_content = self.read_snippet(lecture_file)

        # Extract front matter from source
        front_matter = re.match(r'^---\n(.*?)\n---', lecture_content, re.DOTALL)
        if front_matter:
            lecture_metadata = yaml.safe_load(front_matter.group(1))
        else:
            lecture_metadata = {}

        # Process includes first
        processed_content = self.process_includes(lecture_content)
        processed_content = self.process_media(processed_content)

        # Filter content for notebook
        filtered_content = self.filter_content(processed_content, 'NOTEBOOK')

        # Preprocess math blocks for correct rendering
        filtered_content = self.preprocess_math_blocks(filtered_content)

        # Create notebook
        nb = nbf.v4.new_notebook()

        # Add title and description cell (optional Spanish notebook_* overrides)
        session_num = lecture_metadata.get('session', '1')
        if lecture_metadata.get('notebook_language') == 'es':
            session_label = 'Lección'
        else:
            session_label = 'Practical Session'
        nb_title = lecture_metadata.get('notebook_title') or lecture_metadata.get(
            'title', lecture_file.stem
        )
        nb_description = lecture_metadata.get('notebook_description') or lecture_metadata.get(
            'description', ''
        )
        if lecture_metadata.get('notebook_language') == 'es':
            course_line = '**Curso:**'
            dept_line = '**Departamento del curso:**'
            inst_line = '**Institución del curso:**'
        else:
            course_line = '**Course:**'
            dept_line = '**Course Department:**'
            inst_line = '**Course Institution:**'
        title_cell = nbf.v4.new_markdown_cell(f"""# {session_label} {session_num}: {nb_title}

{nb_description}

---
<font size="3">
{lecture_metadata.get('author', '')}<br>
{lecture_metadata.get('position', '')}<br>
{lecture_metadata.get('department', '')}<br>
{lecture_metadata.get('institution', '')}<br>
{lecture_metadata.get('email', '')}
</font>

---
{course_line} {course_metadata.get('title', '')}<br>
{dept_line} {course_metadata.get('department', '')}<br>
{inst_line} {course_metadata.get('institution', '')}
""")
        nb.cells.append(title_cell)

        # Process content and create cells
        if filtered_content.strip():  # Only process if there's content
            for block_type, source in self._iter_notebook_blocks(filtered_content):
                if block_type == "code":
                    nb.cells.append(nbf.v4.new_code_cell(source))
                else:
                    nb.cells.append(nbf.v4.new_markdown_cell(source))

        # Save notebook
        output_file = output_dir / f"{lecture_file.stem}.ipynb"
        with open(output_file, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)

        if lecture_metadata.get("instructor_only"):
            print(f"[INSTRUCTOR] Local notebook only (not for gh-pages): {output_file}")
            return

        # Create Colab link using the current repository and gh-pages branch
        colab_link = f"https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/{course_metadata.get('course_code', '')}/{lecture_file.stem}.ipynb"

        # Verify the link
        if self.verify_colab_link(colab_link):
            print(f"[OK] Colab notebook link is accessible: {colab_link}")
        else:
            print(f"[WARN] Colab notebook link may not be accessible: {colab_link}")
            print("  Please ensure:")
            print("  1. The notebook is committed to the repository")
            print("  2. The changes are pushed to the gh-pages branch")
            print("  3. The GitHub Pages site is up to date")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate content for lectures and talks')
    parser.add_argument('lectures', nargs='*', help='Lecture files to process (format: course_code/lecture_name)')
    parser.add_argument('--talk', metavar='TALK_ID', help='Process a single talk from scripts/generate_content/talks-sources/<TALK_ID>.md')
    parser.add_argument('--talk-all', action='store_true', help='Process all .md files in scripts/generate_content/talks-sources/')
    parser.add_argument(
        '--slides-only',
        action='store_true',
        help='Generate Marp HTML slides only (skip lecture page and notebook)',
    )
    args = parser.parse_args()

    generator = ContentGenerator(os.getcwd())

    # Talk mode
    if args.talk_all:
        if not generator.talks_sources_dir.exists():
            print(f"Error: Talks sources dir {generator.talks_sources_dir} not found")
            return
        for talk_file in sorted(generator.talks_sources_dir.glob("*.md")):
            generator.process_talk(talk_file)
        return
    if args.talk:
        talk_file = generator.talks_sources_dir / f"{args.talk}.md"
        if not talk_file.exists():
            print(f"Error: Talk file {talk_file} not found")
            return
        generator.process_talk(talk_file)
        return

    # Lecture mode
    if not args.lectures:
        parser.print_help()
        print("\nExamples:")
        print("  python scripts/generate_content/generate_content.py 25-udenar-ml-intro/ai-systems")
        print("  python scripts/generate_content/generate_content.py --slides-only 26-udenar-big-data/l1-introduction")
        print("  python scripts/generate_content/generate_content.py --talk icms-intellectual-debt")
        print("  python scripts/generate_content/generate_content.py --talk-all")
        return

    for lecture_path in args.lectures:
        parts = lecture_path.split('/')
        if len(parts) != 2:
            print(f"Error: Invalid lecture path format. Use course_code/lecture_name")
            continue
        course_code, lecture_name = parts
        lecture_file = generator.sources_dir / course_code / f"{lecture_name}.md"
        if not lecture_file.exists():
            print(f"Error: Lecture file {lecture_file} not found")
            continue
        generator.process_lecture(lecture_file, slides_only=args.slides_only)

if __name__ == "__main__":
    main()
