#!/usr/bin/env python3
"""
YouTube Video Sections Generator

This script fetches all videos from the @PyStructEng YouTube channel
and generates HTML sections for video-scripts.html with placeholders for files.
"""

import yt_dlp
import re
from datetime import datetime
from pathlib import Path


def fetch_channel_videos(channel_handle):
    """
    Fetch all videos from a YouTube channel using yt-dlp.
    
    Args:
        channel_handle: YouTube channel handle (e.g., '@PyStructEng')
    
    Returns:
        List of video dictionaries with title, video_id, url, and upload_date
    """
    channel_url = f"https://www.youtube.com/{channel_handle}/videos"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'playlistend': None,  # Get all videos
        'nocheckcertificate': True,  # Skip SSL certificate verification (for macOS SSL issues)
    }
    
    videos = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching videos from {channel_url}...")
            info = ydl.extract_info(channel_url, download=False)
            
            if 'entries' in info:
                for entry in info['entries']:
                    if entry and entry.get('id'):  # Skip None entries and entries without ID
                        video_id = entry.get('id', '')
                        video_data = {
                            'title': entry.get('title', 'Untitled'),
                            'video_id': video_id,
                            'url': f"https://youtu.be/{video_id}",
                            'upload_date': entry.get('upload_date', ''),
                            'description': entry.get('description', '')
                        }
                        videos.append(video_data)
            
            print(f"Found {len(videos)} videos")
            return videos
            
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []


def format_date(upload_date):
    """
    Convert YYYYMMDD format to "Month DD, YYYY" format.
    
    Args:
        upload_date: Date string in YYYYMMDD format
    
    Returns:
        Formatted date string
    """
    if not upload_date or len(upload_date) != 8:
        return "Date unknown"
    
    try:
        date_obj = datetime.strptime(upload_date, '%Y%m%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return "Date unknown"


def generate_video_section_html(video):
    """
    Generate HTML for a single video section.
    
    Args:
        video: Dictionary with video information
    
    Returns:
        HTML string for the video section
    """
    formatted_date = format_date(video['upload_date'])
    title = video['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    html = f"""            <!-- Video Section -->
            <div class="video-section">
                <h2 class="video-title">{title}</h2>
                <p class="video-date">Published: {formatted_date}</p>
                <a href="{video['url']}" class="video-link" target="_blank">
                    ▶ Watch on YouTube
                </a>
                <div class="scripts-grid">
                    <!-- Add script files here -->
                </div>
            </div>"""
    
    return html


def read_existing_html(file_path):
    """
    Read the existing HTML file and extract the parts we need to preserve.
    
    Args:
        file_path: Path to video-scripts.html
    
    Returns:
        Tuple of (header_html, footer_html) - everything before and after content div
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the content div start
    content_start_match = re.search(r'(<div class="content">)', content)
    
    # Find the closing pattern: </div> for content, then </div> for container, then </body>
    # We'll match from the start of closing content div
    content_end_match = re.search(r'(\s*</div>\s*</div>\s*</body>)', content)
    
    if content_start_match and content_end_match:
        # Header includes everything up to and including the opening content div tag
        header = content[:content_start_match.end()]
        # Footer starts from the closing content div
        footer = content[content_end_match.start():]
        return header, footer
    else:
        # Fallback: try to find just the content div boundaries
        # Find opening tag
        start_idx = content.find('<div class="content">')
        if start_idx != -1:
            # Find the closing </div> that matches the content div
            # Look for pattern: </div> followed by </div> then </body>
            end_pattern = re.search(r'</div>\s*</div>\s*</body>', content)
            if end_pattern:
                header = content[:start_idx + len('<div class="content">')]
                footer = content[end_pattern.start():]
                return header, footer
        
        # Last resort: return the whole file as header, empty footer
        print("Warning: Could not parse HTML structure. Using fallback.")
        return content, ""


def generate_html_file(videos, output_path, dry_run=False, output_text_file=None):
    """
    Generate the complete HTML file with all video sections.
    
    Args:
        videos: List of video dictionaries
        output_path: Path to output HTML file
        dry_run: If True, only print output without writing to file
        output_text_file: Optional path to write complete HTML for copy/paste
    """
    # Read existing HTML to preserve header and footer
    header, footer = read_existing_html(output_path)
    
    # Sort videos by upload date (newest first)
    # Handle videos without upload_date by putting them at the end
    videos_sorted = sorted(
        videos, 
        key=lambda x: x['upload_date'] if x['upload_date'] else '00000000', 
        reverse=True
    )
    
    # Generate video sections HTML
    video_sections = []
    for video in videos_sorted:
        video_sections.append(generate_video_section_html(video))
    
    # Combine everything - match the existing indentation (12 spaces for content div)
    content_html = "        <div class=\"content\">\n" + "\n".join(video_sections) + "\n        </div>"
    
    # Generate complete HTML
    complete_html = header + content_html + footer
    
    if output_text_file:
        # Write complete HTML to text file for copy/paste
        with open(output_text_file, 'w', encoding='utf-8') as f:
            f.write(complete_html)
        print(f"\nComplete HTML written to: {output_text_file}")
    
    if dry_run:
        # Just print what would be generated
        print(f"\nWould generate HTML file with {len(videos_sorted)} video sections")
        print("\n" + "=" * 60)
        print("PREVIEW OF GENERATED CONTENT:")
        print("=" * 60)
        print(content_html)
        print("=" * 60)
    else:
        # Write the complete HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(complete_html)
        
        print(f"Generated HTML file with {len(videos_sorted)} video sections: {output_path}")


def main():
    """Main function to run the script."""
    channel_handle = "@PyStructEng"
    output_file = Path(__file__).parent / "video-scripts.html"
    
    print("=" * 60)
    print("YouTube Video Sections Generator")
    print("=" * 60)
    
    # Fetch videos from channel
    videos = fetch_channel_videos(channel_handle)
    
    if not videos:
        print("No videos found. Exiting.")
        return
    
    # Generate HTML file (dry run - don't write to file)
    # But write complete HTML to a text file for copy/paste
    output_text_file = Path(__file__).parent / "video-scripts-output.txt"
    generate_html_file(videos, output_file, dry_run=True, output_text_file=output_text_file)
    
    print("=" * 60)
    print("Done! You can now manually add script files to each video section.")
    print("=" * 60)


if __name__ == "__main__":
    main()
