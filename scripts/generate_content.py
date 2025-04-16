#!/usr/bin/env python3
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
        self.lectures_dir = self.base_dir / "content" / "_lectures"
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

    def process_includes(self, content):
        """Process include statements in the content."""
        # Pattern to match include statements
        include_pattern = r'{%\s*include\s+([^%}]+)\s*%}'
        
        def replace_include(match):
            include_path = match.group(1).strip()
            # Remove quotes if present
            include_path = include_path.strip('"\'')
            
            # Look for the include file in _includes
            include_file = self.base_dir / "_includes" / include_path
            if not include_file.exists():
                print(f"Warning: Include file {include_file} not found")
                return match.group(0)
                
            # Read and process the include file
            with open(include_file, 'r', encoding='utf-8') as f:
                include_content = f.read()
                
            # Process nested includes
            include_content = self.process_includes(include_content)
            
            return include_content
            
        # Replace all include statements
        processed_content = re.sub(include_pattern, replace_include, content)
        
        return processed_content

    def filter_content(self, content, target):
        """Filter content based on markers for specific target (RENDER, SLIDES, or NOTEBOOK)."""
        # Remove front matter first
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Define patterns for each marker type
        patterns = {
            'ALL': r'<!--\s*ALL:\s*-->(.*?)(?=<!--|\Z)',
            'TARGET': fr'<!--\s*{target}:\s*-->(.*?)(?=<!--|\Z)',
            'RENDER_TARGET': fr'<!--\s*RENDER\+{target}:\s*-->(.*?)(?=<!--|\Z)',
            'TARGET_NOTEBOOK': fr'<!--\s*{target}\+NOTEBOOK:\s*-->(.*?)(?=<!--|\Z)',
            'SLIDES_TARGET': fr'<!--\s*SLIDES\+{target}:\s*-->(.*?)(?=<!--|\Z)',
        }
        
        filtered_content = []
        
        # Extract content for each pattern
        for pattern_type, pattern in patterns.items():
            matches = re.finditer(pattern, content_without_frontmatter, re.DOTALL)
            for match in matches:
                content_part = match.group(1).strip()
                if content_part:  # Only add non-empty content
                    filtered_content.append(content_part)
        
        # Join all filtered content with double newlines
        return '\n\n'.join(filtered_content)

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
        
        # Generate content with course-specific paths
        self.generate_rendered_lecture(lecture_file, course_lectures_dir, course_metadata)
        self.generate_slides(lecture_file, course_slides_dir)
        self.generate_notebook(lecture_file, course_notebooks_dir, course_metadata)

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
        
        # Filter content for rendered markdown
        filtered_content = self.filter_content(content, 'RENDER')
        
        # Process content
        processed_content = self.process_includes(filtered_content)
        processed_content = self.process_media(processed_content)
        
        index_url = "{ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'}"
        # Create rendered content with metadata and resources
        rendered_content = f"""---
{yaml.dump(metadata, default_flow_style=False)}---

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    async function main() {{
        let pyodide = await loadPyodide({index_url});
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
    }}
    main();
</script>

<div class="lecture-resources">
  <p>
    <a href="/assets/slides/{course_metadata.get('course_code', '')}/{lecture_file.stem}.pdf" target="_blank">[PDF Slides]</a>
    <a href="/assets/slides/{course_metadata.get('course_code', '')}/{lecture_file.stem}.html" target="_blank">[HTML Slides]</a>
    <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/{course_metadata.get('course_code', '')}/{lecture_file.stem}.ipynb" target="_blank">[Colab Notebook]</a>
  </p>
</div>

{processed_content}
"""
        
        # Save rendered lecture
        output_file = output_dir / lecture_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

    def generate_slides(self, lecture_file, output_dir):
        """Generate Marp slides from lecture content."""
        lecture_content = self.read_snippet(lecture_file)
        
        # Remove front matter first
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', lecture_content, flags=re.DOTALL)
        
        # Find all content blocks with their markers
        content_blocks = []
        
        # Pattern to match any of our markers and their content
        pattern = r'<!--\s*(ALL|SLIDES|SLIDES\+NOTEBOOK|RENDER\+SLIDES):\s*-->(.*?)(?=<!--|\Z)'
        
        # Find all matches in order
        matches = re.finditer(pattern, content_without_frontmatter, re.DOTALL)
        for match in matches:
            marker_type = match.group(1)
            content = match.group(2).strip()
            if content:  # Only add non-empty content
                content_blocks.append(content)
        
        # Join all content blocks in their original order
        processed_content = '\n\n'.join(content_blocks)
        
        # Process content
        processed_content = self.process_includes(processed_content)
        processed_content = self.process_media(processed_content)
        
        # Split content into slides based on headings
        slides = []
        current_slide = []
        
        # Split content into lines and process
        lines = processed_content.split('\n')
        for line in lines:
            # If line is a heading (starts with #), start a new slide
            if line.strip().startswith('#') and current_slide:
                slides.append('\n'.join(current_slide))
                current_slide = []
            current_slide.append(line)
        
        # Add the last slide
        if current_slide:
            slides.append('\n'.join(current_slide))
        
        # Join slides with Marp slide separator
        slides_content = '\n\n---\n\n'.join(slides)
        
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
        
        # Create Marp slides
        marp_content = f"""---
marp: true
theme: default
paginate: true
header: "Session {metadata.get('session', '1')} - {metadata.get('title', '')}"
footer: ""
style: |
  :root {{
    --primary-color: #00244A;    /* Blue navy */
    --secondary-color: #00BDB6;  /* Cambridge warm blue */
    --accent-color: #00BDB6;     /* Cambridge warm blue */
    --text-color: #00244A;       /* Blue navy for text */
    --background-color: #FFFFFF; /* White background */
    --progress-color: #00244A;   /* Blue navy for progress bar */
  }}
  
  section {{
    background-color: var(--background-color);
    color: var(--text-color);
    padding: 40px;
    font-size: 28px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }}
  
  h1 {{
    font-size: 48px;
    color: var(--text-color);
    margin-bottom: 20px;
    padding-bottom: 10px;
  }}
  
  h2 {{
    font-size: 40px;
    color: var(--text-color);
    margin-bottom: 15px;
  }}
  
  h3 {{
    font-size: 32px;
    color: var(--text-color);
    margin-bottom: 10px;
  }}
  
  ul, ol {{
    margin-left: 30px;
    margin-top: 15px;
  }}
  
  li {{
    margin-bottom: 10px;
  }}
  
  img {{
    max-width: 80%;
    margin: 20px auto;
    display: block;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }}
  
  code {{
    font-size: 24px;
    background-color: rgba(10, 25, 47, 0.1);
    color: var(--text-color);
    padding: 4px 8px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
  }}
  
  pre {{
    background-color: rgba(10, 25, 47, 0.1);
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
  }}
  
  /* Link styling */
  a {{
    color: var(--secondary-color);
    text-decoration: none;
  }}
  
  a:hover {{
    text-decoration: underline;
  }}
  
  /* Pagination styling */
  section::before {{
    font-size: 0.6em;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    position: absolute;
    text-align: right;
    top: 96.2%;
    width: 100%;
    right: 0;
    left: -0.5em;
    color: var(--secondary-color);
  }}
  
  /* Hide default Marp pagination */
  section::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: calc(100% * var(--marp-progress));
    height: 4px;
    background: var(--accent-color);
    z-index: 2;
  }}
  
  /* Hide pagination on lead slides */
  section.lead::before {{
    display: none;
  }}
  
  /* Hide progress bar on lead slides */
  section.lead::after {{
    display: none;
  }}
  
  /* Header styling */
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
  }}

  /* Title slide specific styling */
  section.lead h1 {{
    margin-bottom: 10px;
  }}
  
  section.lead p {{
    font-size: 24px;
    margin: 5px 0;
    line-height: 1.2;
  }}

  /* Hide header on lead slides */
  section.lead header {{
    display: none;
  }}

  /* Center content only on the last slide */
  section.lead.last-slide {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 100vh;
  }}

  section.lead.last-slide h1 {{
    margin-bottom: 20px;
  }}

  section.lead.last-slide p {{
    margin: 10px 0;
  }}

---

<!-- _class: lead -->
# {metadata.get('title', '')}
<p><b>{metadata.get('author', '')}</b></p>
<p>{metadata.get('position', '')}</p>
<p>{metadata.get('department', '')}</p>
<p>{metadata.get('institution', '')}</p>
<p><a href="mailto:{metadata.get('email', '')}">{metadata.get('email', '')}</a></p>

---

{slides_content}

---

<!-- _class: lead last-slide -->
# Many Thanks!
<p><a href="mailto:{metadata.get('email', '')}">{metadata.get('email', '')}</a></p>
"""
        
        # Save markdown slides
        output_file = output_dir / f"{lecture_file.stem}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(marp_content)
        
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
            
            # Generate PDF
            if isinstance(marp_cmd, list):
                pdf_cmd = marp_cmd + [
                    str(output_file),
                    '--pdf',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.pdf")
                ]
            else:
                pdf_cmd = [
                    marp_cmd,
                    str(output_file),
                    '--pdf',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.pdf")
                ]
            
            print(f"Running command: {' '.join(pdf_cmd)}")
            subprocess.run(pdf_cmd, check=True)
            
            # Generate HTML
            if isinstance(marp_cmd, list):
                html_cmd = marp_cmd + [
                    str(output_file),
                    '--html',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.html")
                ]
            else:
                html_cmd = [
                    marp_cmd,
                    str(output_file),
                    '--html',
                    '--allow-local-files',
                    '-o', str(output_dir / f"{lecture_file.stem}.html")
                ]
            
            print(f"Running command: {' '.join(html_cmd)}")
            subprocess.run(html_cmd, check=True)
            
            print(f"✓ Successfully generated slides for {lecture_file.stem}")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to generate slides: {e}")
            print(f"Command output: {e.output.decode() if e.output else 'No output'}")
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

    def generate_notebook(self, lecture_file, output_dir, course_metadata):
        """Generate Jupyter notebook from lecture content."""
        lecture_content = self.read_snippet(lecture_file)
        
        # Filter content for notebook
        filtered_content = self.filter_content(lecture_content, 'NOTEBOOK')
        
        # Process content
        processed_content = self.process_includes(filtered_content)
        processed_content = self.process_media(processed_content)
        
        # Create notebook
        nb = nbf.v4.new_notebook()
        
        # Add title cell
        title_cell = nbf.v4.new_markdown_cell(f"# {lecture_file.stem}")
        nb.cells.append(title_cell)
        
        # Process content and create cells
        sections = processed_content.split('\n\n')
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
    parser = argparse.ArgumentParser(description='Generate content for lectures')
    parser.add_argument('lectures', nargs='+', help='Names of lecture files to process (format: course_code/lecture_name)')
    args = parser.parse_args()

    generator = ContentGenerator(os.getcwd())
    
    # Process each specified lecture
    for lecture_path in args.lectures:
        # Split course_code/lecture_name
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