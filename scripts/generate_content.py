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

class ContentGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.snippets_dir = self.base_dir / "content" / "_snippets"
        self.lectures_dir = self.base_dir / "content" / "_lectures"
        self.assets_dir = self.base_dir / "assets"
        self.media_dir = self.base_dir / "assets" / "media"
        
        # Create output directories in assets
        (self.assets_dir / "slides").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "notebooks").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "media").mkdir(parents=True, exist_ok=True)
        
        # Initialize mime type detector
        self.mime = magic.Magic(mime=True)

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

    def generate_slides(self, lecture_file):
        """Generate Marp slides from lecture content."""
        lecture_content = self.read_snippet(lecture_file)
        
        # Extract front matter
        front_matter = re.match(r'^---\n(.*?)\n---', lecture_content, re.DOTALL)
        if front_matter:
            metadata = yaml.safe_load(front_matter.group(1))
            lecture_content = lecture_content[front_matter.end():]
        else:
            metadata = {
                'title': lecture_file.stem,
                'session': '1',
                'description': 'Lecture'
            }
        
        # Process media content
        lecture_content = self.process_media(lecture_content)
        
        # Create Marp slides
        slides_content = f"""---
marp: true
theme: default
paginate: true
header: "{metadata.get('title', '')}"
footer: "Session {metadata.get('session', '1')}"
style: |
  section {{
    background-color: white;
  }}
  img {{
    max-width: 100%;
    height: auto;
  }}
  video {{
    max-width: 100%;
  }}

# {metadata.get('title', '')}
## Session {metadata.get('session', '1')}: {metadata.get('description', '')}

"""
        
        # Process content and create slides
        sections = lecture_content.split('\n\n')
        for section in sections:
            if section.strip():
                slides_content += f"\n---\n\n{section}\n"
        
        # Save markdown slides
        output_file = self.assets_dir / "slides" / f"{lecture_file.stem}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(slides_content)
        
        # Generate PDF slides using Marp CLI
        try:
            subprocess.run([
                'marp',
                str(output_file),
                '--pdf',
                '--allow-local-files',
                '-o', str(self.assets_dir / "slides" / f"{lecture_file.stem}.pdf")
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to generate PDF slides: {e}")
        except FileNotFoundError:
            print("Warning: Marp CLI not found. Please install it with: npm install -g @marp-team/marp-cli")

    def generate_notebook(self, lecture_file):
        """Generate Jupyter notebook from lecture content."""
        lecture_content = self.read_snippet(lecture_file)
        
        # Process media content
        lecture_content = self.process_media(lecture_content)
        
        # Create notebook
        nb = nbf.v4.new_notebook()
        
        # Add title cell
        title_cell = nbf.v4.new_markdown_cell(f"# {lecture_file.stem}")
        nb.cells.append(title_cell)
        
        # Add Colab setup cell
        colab_setup = """# Mount Google Drive (if needed)
from google.colab import drive
drive.mount('/content/drive')

# Install required packages
!pip install -r requirements.txt"""
        nb.cells.append(nbf.v4.new_code_cell(colab_setup))
        
        # Process content and create cells
        sections = lecture_content.split('\n\n')
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
        output_file = self.assets_dir / "notebooks" / f"{lecture_file.stem}.ipynb"
        with open(output_file, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        
        # Create Colab link
        colab_link = f"https://colab.research.google.com/github/{os.getenv('GITHUB_USERNAME', 'yourusername')}/course-notebooks/blob/main/{lecture_file.stem}.ipynb"
        print(f"Colab notebook link: {colab_link}")

    def process_lecture(self, lecture_file):
        """Process a lecture file to generate all formats."""
        print(f"Processing {lecture_file}...")
        self.generate_slides(lecture_file)
        self.generate_notebook(lecture_file)

def main():
    generator = ContentGenerator(os.getcwd())
    
    # Process all lectures
    for lecture_file in generator.lectures_dir.glob("*.md"):
        generator.process_lecture(lecture_file)

if __name__ == "__main__":
    main() 