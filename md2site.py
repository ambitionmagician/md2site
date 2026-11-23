#!/usr/bin/env python3
import argparse
import markdown
import os
import re
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to HTML for a static site.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('src_dir', type=Path, help='Source directory containing .md files')
    parser.add_argument('out_dir', type=Path, help='Output directory for generated .html files')
    parser.add_argument('--site-title', default='Site', help='Title for the website (default: "Site")')
    parser.add_argument('--css', type=Path, help='External stylesheet to link instead of inline CSS')
    return parser.parse_args()

def get_title(md_content, filename):
    for line in md_content.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return Path(filename).stem

def convert_md_to_html(md_content, title, site_title, css_path=None):
    html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])
    # Rewrite relative links to other Markdown pages so they point at the
    # generated .html files instead of the .md sources.
    html_content = re.sub(r'href="([^"#]+)\.md(["#])', r'href="\1.html\2', html_content)
    html_content = re.sub(r'href="([^"#]+)\.md"', r'href="\1.html"', html_content)
    
    if css_path:
        css_link = f'<link rel="stylesheet" href="{css_path}">'
    else:
        css_link = '<style>body { font-family: sans-serif; margin: 2em; } a { color: #0066cc; }</style>'
    
    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {site_title}</title>
    {css_link}
</head>
<body>
{html_content}
</body>
</html>'''
    return template

def process_markdown_files(src_dir, out_dir, site_title, css_path):
    md_files = []
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.md'):
                src_path = Path(root) / file
                rel_path = src_path.relative_to(src_dir)
                md_files.append((src_path, rel_path))
    
    md_files.sort(key=lambda x: str(x[1]))
    
    for src_path, rel_path in md_files:
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except Exception as e:
            print(f"Error reading {src_path}: {e}", file=sys.stderr)
            continue
        
        title = get_title(md_content, src_path.name)
        html_content = convert_md_to_html(md_content, title, site_title, css_path)
        
        out_path = out_dir / rel_path.with_suffix('.html')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Written: {out_path}")
        except Exception as e:
            print(f"Error writing {out_path}: {e}", file=sys.stderr)
            continue

def generate_index(out_dir, site_title, css_path):
    html_files = []
    
    for root, dirs, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                file_path = Path(root) / file
                rel_path = file_path.relative_to(out_dir)
                html_files.append(rel_path)
    
    html_files.sort(key=lambda x: str(x))
    
    links = []
    for html_file in html_files:
        href = html_file.as_posix()
        title = html_file.with_suffix('').name.replace('-', ' ').title()
        links.append(f'    <li><a href="{href}">{title}</a></li>')
    
    links_html = '\n'.join(links)
    
    if css_path:
        css_link = f'<link rel="stylesheet" href="{css_path}">'
    else:
        css_link = '<style>body { font-family: sans-serif; margin: 2em; } a { color: #0066cc; }</style>'
    
    index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    {css_link}
</head>
<body>
    <h1>{site_title}</h1>
    <ul>
{links_html}
    </ul>
</body>
</html>'''
    
    index_path = out_dir / 'index.html'
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"Written: {index_path}")
    except Exception as e:
        print(f"Error writing {index_path}: {e}", file=sys.stderr)

def main():
    args = parse_args()
    
    src_dir = args.src_dir.resolve()
    out_dir = args.out_dir.resolve()
    site_title = args.site_title
    css_path = args.css
    
    if not src_dir.exists():
        print(f"Error: Source directory '{src_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not src_dir.is_dir():
        print(f"Error: '{src_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory '{out_dir}': {e}", file=sys.stderr)
        sys.exit(1)
    
    if css_path:
        css_path = Path(css_path).name
    
    process_markdown_files(src_dir, out_dir, site_title, css_path)
    generate_index(out_dir, site_title, css_path)

if __name__ == '__main__':
    main()
