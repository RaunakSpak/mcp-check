#!/usr/bin/env python3
"""
MCP Server for Enecovery Website
Provides tools to read, search, and extract information from HTML pages
"""

import re
from pathlib import Path
from typing import Optional
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

try:
    from fastmcp import FastMCP
except ImportError:
    raise ImportError(
        "FastMCP is required. Install it with: pip install fastmcp\n"
        "Or use: pip install -r requirements.txt"
    )

# Initialize the MCP server
mcp = FastMCP("Enecovery Website MCP Server")

# Get the base directory (where HTML files are located)
BASE_DIR = Path(__file__).parent.absolute()


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML while preserving structure"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.current_tag = None
        self.in_script = False
        self.in_style = False
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in ['script', 'style']:
            if tag == 'script':
                self.in_script = True
            elif tag == 'style':
                self.in_style = True
                
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script = False
            self.in_style = False
        if tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'br']:
            self.text.append('\n')
        self.current_tag = None
            
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            cleaned = data.strip()
            if cleaned:
                self.text.append(cleaned)
                
    def get_text(self):
        return ' '.join(self.text).strip()


def extract_metadata(html_content: str) -> dict:
    """Extract metadata from HTML content"""
    metadata = {}
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
    if desc_match:
        metadata['description'] = desc_match.group(1).strip()
    
    # Extract meta keywords
    keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
    if keywords_match:
        metadata['keywords'] = keywords_match.group(1).strip()
    
    # Extract all headings
    headings = {
        'h1': re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL),
        'h2': re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.IGNORECASE | re.DOTALL),
        'h3': re.findall(r'<h3[^>]*>(.*?)</h3>', html_content, re.IGNORECASE | re.DOTALL),
    }
    # Clean headings
    for level in headings:
        headings[level] = [re.sub(r'<[^>]+>', '', h).strip() for h in headings[level]]
    metadata['headings'] = headings
    
    # Extract links
    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html_content, re.IGNORECASE | re.DOTALL)
    metadata['links'] = [(link[0], re.sub(r'<[^>]+>', '', link[1]).strip()) for link in links[:20]]  # Limit to 20 links
    
    return metadata


def read_html_file(filepath: str) -> Optional[str]:
    """Read HTML file content"""
    try:
        full_path = BASE_DIR / filepath
        if not full_path.exists():
            return None
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None


def list_html_files() -> list:
    """List all HTML files in the base directory"""
    html_files = []
    for file in BASE_DIR.glob('*.html'):
        html_files.append(file.name)
    return sorted(html_files)


def search_in_html(query: str, filepath: Optional[str] = None) -> list:
    """Search for query in HTML files"""
    results = []
    files_to_search = [filepath] if filepath else list_html_files()
    
    for filename in files_to_search:
        content = read_html_file(filename)
        if content:
            # Case-insensitive search
            if query.lower() in content.lower():
                # Extract context around matches
                lines = content.split('\n')
                matches = []
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        context = '\n'.join(lines[start:end])
                        matches.append({
                            'line': i + 1,
                            'context': context[:500]  # Limit context length
                        })
                
                if matches:
                    results.append({
                        'file': filename,
                        'matches': matches[:5]  # Limit to 5 matches per file
                    })
    
    return results


@mcp.tool()
def read_page(filepath: str) -> str:
    """Read the content of an HTML page. Returns the full HTML content and extracted text.
    
    Args:
        filepath: Path to the HTML file (e.g., 'index.html', 'aboutus.html')
    """
    content = read_html_file(filepath)
    if content is None:
        return f"Error: Could not read file '{filepath}' or file does not exist."
    
    # Extract text for easier reading
    parser = HTMLTextExtractor()
    parser.feed(content)
    text_content = parser.get_text()
    
    if len(text_content) > 5000:
        return f"=== Content of {filepath} ===\n\nHTML Content Length: {len(content)} characters\n\nExtracted Text:\n{text_content[:5000]}..."
    else:
        return f"=== Content of {filepath} ===\n\n{text_content}"


@mcp.tool()
def extract_text(filepath: str) -> str:
    """Extract plain text from an HTML page, removing all HTML tags.
    
    Args:
        filepath: Path to the HTML file
    """
    content = read_html_file(filepath)
    if content is None:
        return f"Error: Could not read file '{filepath}' or file does not exist."
    
    parser = HTMLTextExtractor()
    parser.feed(content)
    text = parser.get_text()
    
    return text


@mcp.tool()
def get_metadata(filepath: str) -> str:
    """Extract metadata from an HTML page (title, description, keywords, headings, links).
    
    Args:
        filepath: Path to the HTML file
    """
    content = read_html_file(filepath)
    if content is None:
        return f"Error: Could not read file '{filepath}' or file does not exist."
    
    metadata = extract_metadata(content)
    
    result = f"=== Metadata for {filepath} ===\n\n"
    result += f"Title: {metadata.get('title', 'N/A')}\n\n"
    result += f"Description: {metadata.get('description', 'N/A')}\n\n"
    result += f"Keywords: {metadata.get('keywords', 'N/A')}\n\n"
    
    result += "Headings:\n"
    for level in ['h1', 'h2', 'h3']:
        if metadata['headings'][level]:
            result += f"  {level.upper()}: {', '.join(metadata['headings'][level][:10])}\n"
    
    result += f"\nLinks ({len(metadata['links'])} found):\n"
    for link, text in metadata['links'][:10]:
        result += f"  - {text}: {link}\n"
    
    return result


@mcp.tool()
def list_pages() -> str:
    """List all available HTML pages in the website."""
    pages = list_html_files()
    result = f"=== Available HTML Pages ({len(pages)}) ===\n\n"
    for i, page in enumerate(pages, 1):
        result += f"{i}. {page}\n"
    
    return result


@mcp.tool()
def search_content(query: str, filepath: Optional[str] = None) -> str:
    """Search for a query string across HTML files. Returns files and line numbers where matches are found.
    
    Args:
        query: Search query string
        filepath: Optional: specific file to search in. If not provided, searches all files.
    """
    results = search_in_html(query, filepath)
    
    if not results:
        return f"No matches found for '{query}'"
    
    result_text = f"=== Search Results for '{query}' ===\n\n"
    for item in results:
        result_text += f"File: {item['file']}\n"
        result_text += f"Matches found: {len(item['matches'])}\n"
        for match in item['matches']:
            result_text += f"  Line {match['line']}:\n  {match['context'][:200]}...\n\n"
    
    return result_text


@mcp.tool()
def get_sitemap() -> str:
    """Get the sitemap information showing all pages and their priorities."""
    sitemap_path = BASE_DIR / "sitemap.xml"
    if not sitemap_path.exists():
        return "Sitemap.xml not found."
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        result = "=== Sitemap Information ===\n\n"
        urls = []
        
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            priority = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
            lastmod = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            
            if loc is not None:
                url_text = loc.text
                # Extract filename from URL
                filename = url_text.split('/')[-1] if '/' in url_text else url_text
                priority_text = priority.text if priority is not None else "N/A"
                lastmod_text = lastmod.text if lastmod is not None else "N/A"
                
                urls.append({
                    'filename': filename,
                    'priority': priority_text,
                    'lastmod': lastmod_text
                })
        
        # Sort by priority
        urls.sort(key=lambda x: float(x['priority']) if x['priority'] != 'N/A' else 0, reverse=True)
        
        for url in urls[:50]:  # Limit to top 50
            result += f"{url['filename']} (Priority: {url['priority']}, Last Modified: {url['lastmod']})\n"
        
        if len(urls) > 50:
            result += f"\n... and {len(urls) - 50} more pages"
        
        return result
    except Exception as e:
        return f"Error reading sitemap: {str(e)}"


if __name__ == "__main__":
    mcp.run()
