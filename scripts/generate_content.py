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

or from the command line:
```
python scripts/generate_content.py course_code/lecture_name
```
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
from urllib.parse import urlparse
import argparse

class ContentGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.sources_dir = self.base_dir / "scripts" / "lectures-sources"
        self.talks_sources_dir = self.base_dir / "scripts" / "talks-sources"
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
                print("⚠ npm not found in PATH")
                print("\nPlease install Node.js and npm:")
                print("1. Download Node.js from https://nodejs.org/")
                print("2. Run the installer")
                print("3. Check 'Add to PATH' during installation")
                print("4. Restart your terminal after installation")
                return False

            print(f"✓ Found npm at: {npm_cmd}")

            # Check npm global installation
            try:
                npm_prefix = subprocess.check_output([npm_cmd, 'config', 'get', 'prefix'], text=True).strip()
                print(f"✓ npm global prefix: {npm_prefix}")

                # Check if Marp is installed globally
                try:
                    marp_version = subprocess.check_output([npm_cmd, 'list', '-g', '@marp-team/marp-cli'], text=True)
                    print("✓ Marp CLI is installed globally")
                    print(f"  Installation details:\n{marp_version}")
                except subprocess.CalledProcessError:
                    print("⚠ Marp CLI is not installed globally")
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
                        print(f"✓ Found Marp at: {location}")
                        found = True
                    else:
                        print(f"✗ Not found: {location}")

                if not found:
                    print("\n⚠ Marp executable not found in common locations")
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
                        print(f"✓ npm bin directory in PATH: {dir_path}")
                    else:
                        print(f"✗ npm bin directory not in PATH: {dir_path}")
                        print("  You may need to add this to your PATH")

                # Try running marp directly
                try:
                    marp_version = subprocess.check_output(['marp', '--version'], text=True)
                    print(f"\n✓ Marp CLI is accessible: {marp_version.strip()}")
                    return True
                except:
                    print("\n⚠ Marp CLI is not accessible from PATH")
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

    def preprocess_math_blocks(self, content):
        """
        Ensure block math ($$...$$) is always at the root level in Markdown output, not inside HTML tags.
        This helps Marp/Markdown/MathJax render AI/ML equations (matrices, vectors, sums, integrals, etc.) correctly.
        After rendering, the expressions are wrapped in p tags for consistent styling.
        """
        import re

        # First handle block math
        block_math_pattern = re.compile(r'(\${2}.*?\${2})', re.DOTALL)
        math_blocks = []
        def math_replacer(match):
            idx = len(math_blocks)
            math_blocks.append(match.group(1))
            return f'__MATH_BLOCK_{idx}__'

        # Replace all block math with placeholders
        content_with_placeholders = block_math_pattern.sub(math_replacer, content)

        # Now handle inline math - look for \(...\) pattern
        inline_math_pattern = re.compile(r'\\\((.*?)\\\)')
        def inline_math_replacer(match):
            math_expr = match.group(1)
            # Only wrap in p tags if not already inside a p tag
            if not re.search(r'<p[^>]*>.*?\\\(' + re.escape(math_expr) + r'\\\).*?</p>', content_with_placeholders):
                return f'${math_expr}$'
            return f'${math_expr}$'

        # Replace inline math with wrapped versions
        content_with_placeholders = inline_math_pattern.sub(inline_math_replacer, content_with_placeholders)

        # Move block math placeholders to root level
        def move_placeholder_to_root(match):
            return f'\n{match.group(0)}\n'
        content_with_placeholders = re.sub(r'__MATH_BLOCK_\d+__', move_placeholder_to_root, content_with_placeholders)

        # Remove extra blank lines
        content_with_placeholders = re.sub(r'\n{3,}', '\n\n', content_with_placeholders)

        # Replace placeholders with actual math blocks
        for idx, math_block in enumerate(math_blocks):
            content_with_placeholders = content_with_placeholders.replace(f'__MATH_BLOCK_{idx}__', math_block)

        # After all math is processed, wrap rendered math expressions in p tags
        # This will happen after Marp/MathJax has rendered the expressions
        content_with_placeholders = re.sub(
            r'(<span class="math inline">.*?</span>)',
            r'<p>\1</p>',
            content_with_placeholders
        )
        content_with_placeholders = re.sub(
            r'(<span class="math display">.*?</span>)',
            r'<p>\1</p>',
            content_with_placeholders
        )

        return content_with_placeholders

    def process_lecture(self, lecture_file):
        """Process a lecture file to generate all formats."""
        print(f"Processing {lecture_file}...")

        # Get course code from path
        course_code = lecture_file.parent.name

        # Get course metadata
        course_metadata = self.get_course_metadata(course_code)

        # Create course-specific directories
        course_lectures_dir = self.lectures_dir / course_code
        course_slides_dir = self.assets_dir / "slides" / course_code
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
                    protected_lines.append(re.sub(r'^\s*#', r'\1<comment>', line))
                else:
                    protected_lines.append(line)
            return f'```python\n{chr(10).join(protected_lines)}\n```'

        # Replace comments in all code blocks
        content = re.sub(code_block_pattern, protect_comments, content, flags=re.DOTALL)

        # Clean code blocks to remove any markdown/HTML artifacts
        content = self.clean_code_blocks(content)

        # Generate content with course-specific paths
        self.generate_rendered_lecture(lecture_file, course_lectures_dir, course_metadata)
        self.generate_slides(lecture_file, course_slides_dir)
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
        config_file = self.base_dir / "_config.yml"
        base_url = "https://cabrerac.github.io"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as cf:
                config_content = cf.read()
                url_match = re.search(r'url:\s*["\']([^"\']+)["\']', config_content)
                if url_match:
                    base_url = url_match.group(1).strip().rstrip('/')
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
        self.update_talks_yml(talks_list)
        print(f"✓ Updated _data/talks.yml for {talk_id}")

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
            print(f"✓ Wrote talk page {output_file}")

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

        index_url = "{ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'}"
        # Create rendered content with metadata and resources
        rendered_content = f"""---
{yaml.dump(metadata, default_flow_style=False)}---

<link rel=\"stylesheet\" href=\"/assets/css/slides.css\">
<div class=\"lecture-resources\">
  <p>
    <a href=\"/assets/slides/{course_metadata.get('course_code', '')}/{lecture_file.stem}.html\" target=\"_blank\">[HTML Slides]</a>
    <a href=\"https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/{course_metadata.get('course_code', '')}/{lecture_file.stem}.ipynb\" target=\"_blank\">[Colab Notebook]</a>
    <a href=\"/teaching/{course_metadata.get('course_code', '')}/">[Back to Course]</a>
  </p>
</div>

{filtered_content}
"""

        # Save rendered lecture
        output_file = output_dir / lecture_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

    def generate_slides(self, lecture_file, output_dir):
        """Generate Marp slides from lecture content."""
        lecture_content = self.read_snippet(lecture_file)

        # Process includes first
        processed_content = self.process_includes(lecture_content)
        processed_content = self.process_media(processed_content)

        # Filter content for slides
        filtered_content = self.filter_content(processed_content, 'SLIDES')
        # Preprocess math blocks for correct rendering
        filtered_content = self.preprocess_math_blocks(filtered_content)

        # Split into slide blocks using # and ## as slide boundaries
        slide_blocks = []
        current_block = []
        lines = filtered_content.split('\n')
        for line in lines:
            if re.match(r'^#{1,2} ', line.strip()):
                if current_block:
                    slide_blocks.append('\n'.join(current_block))
                    current_block = []
            current_block.append(line)
        if current_block:
            slide_blocks.append('\n'.join(current_block))

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
        # Template for slides (removing duplicated lead sections)
        marp_template = f"""---
marp: true
theme: default
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

  section::before {{
    font-size: 0.6em;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    position: absolute;
    text-align: right;
    bottom: 1em;
    right: 1em;
    color: var(--secondary-color);
  }}

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

        # Create Marp slides for HTML (all slides)
        html_content = f"""
<!-- _class: lead -->
# {metadata.get('title', '')}
<p style="color: var(--text-color);"><b>{metadata.get('author', '')}</b></p>
<p style="color: var(--text-color);">{metadata.get('position', '')}</p>
<p style="color: var(--text-color);">{metadata.get('department', '')}</p>
<p style="color: var(--text-color);">{metadata.get('institution', '')}</p>
<p style="color: var(--accent-color);"><a href="mailto:{metadata.get('email', '')}" style="color: var(--accent-color);">{metadata.get('email', '')}</a></p>

---

{slides_content}

---

<!-- _class: lead last-slide -->
# Many Thanks!
<p style="color: var(--accent-color);"><a href="mailto:{metadata.get('email', '')}" style="color: var(--accent-color);">{metadata.get('email', '')}</a></p>
"""

        # Create Marp slides for PDF (only marked slides)
        pdf_content = f"""
<!-- _class: lead -->
# {metadata.get('title', '')}
<p style="color: var(--text-color);"><b>{metadata.get('author', '')}</b></p>
<p style="color: var(--text-color);">{metadata.get('position', '')}</p>
<p style="color: var(--text-color);">{metadata.get('department', '')}</p>
<p style="color: var(--text-color);">{metadata.get('institution', '')}</p>
<p style="color: var(--text-color);">{metadata.get('email', '')}</p>

---

{pdf_slides_content}

---

<!-- _class: lead last-slide -->
# Many Thanks!
<p style="color: var(--accent-color);"><a href="mailto:{metadata.get('email', '')}" style="color: var(--accent-color);">{metadata.get('email', '')}</a></p>
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

            # Generate HTML from the HTML-specific file
            if isinstance(marp_cmd, list):
                html_cmd = marp_cmd + [
                    str(html_file),
                    '--html',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.html")
                ]
            else:
                html_cmd = [
                    marp_cmd,
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

            print(f"✓ Successfully generated slides for {lecture_file.stem}")
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

        # Add title and description cell
        title_cell = nbf.v4.new_markdown_cell(f"""# Practical Session {lecture_metadata.get('session', '1')}: {lecture_metadata.get('title', lecture_file.stem)}

{lecture_metadata.get('description', '')}

---
<font size="3">
{lecture_metadata.get('author', '')}<br>
{lecture_metadata.get('position', '')}<br>
{lecture_metadata.get('department', '')}<br>
{lecture_metadata.get('institution', '')}<br>
{lecture_metadata.get('email', '')}
</font>

---
**Course:** {course_metadata.get('title', '')}<br>
**Course Department:** {course_metadata.get('department', '')}<br>
**Course Institution:** {course_metadata.get('institution', '')}
""")
        nb.cells.append(title_cell)

        # Process content and create cells
        if filtered_content.strip():  # Only process if there's content
            sections = filtered_content.split('\n\n')
            for section in sections:
                if section.strip():
                    if section.startswith('```python'):
                        # Code cell
                        code = section.split('\n', 1)[1].rsplit('\n', 1)[0]
                        nb.cells.append(nbf.v4.new_code_cell(code))
                    else:
                        # Markdown cell
                        nb.cells.append(nbf.v4.new_markdown_cell(section))

        # Save notebook
        output_file = output_dir / f"{lecture_file.stem}.ipynb"
        with open(output_file, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)

        # Create Colab link using the current repository and gh-pages branch
        colab_link = f"https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/{course_metadata.get('course_code', '')}/{lecture_file.stem}.ipynb"

        # Verify the link
        if self.verify_colab_link(colab_link):
            print(f"✓ Colab notebook link is accessible: {colab_link}")
        else:
            print(f"⚠ Colab notebook link may not be accessible: {colab_link}")
            print("  Please ensure:")
            print("  1. The notebook is committed to the repository")
            print("  2. The changes are pushed to the gh-pages branch")
            print("  3. The GitHub Pages site is up to date")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate content for lectures and talks')
    parser.add_argument('lectures', nargs='*', help='Lecture files to process (format: course_code/lecture_name)')
    parser.add_argument('--talk', metavar='TALK_ID', help='Process a single talk from scripts/talks-sources/<TALK_ID>.md')
    parser.add_argument('--talk-all', action='store_true', help='Process all .md files in scripts/talks-sources/')
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
        print("  python scripts/generate_content.py 25-udenar-ml-intro/ai-systems")
        print("  python scripts/generate_content.py --talk icms-intellectual-debt")
        print("  python scripts/generate_content.py --talk-all")
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
        generator.process_lecture(lecture_file)

if __name__ == "__main__":
    main()
