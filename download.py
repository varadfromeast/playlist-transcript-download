import os
import sys
import json
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi

def get_videos_from_playlist(url):
    print("Fetching playlist videos...")
    result = subprocess.run(
        ["yt-dlp", "-J", "--flat-playlist", url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error fetching playlist:", result.stderr)
        return []
    
    videos = []
    try:
        data = json.loads(result.stdout)
        if 'entries' in data:
            for entry in data['entries']:
                if 'id' in entry:
                    videos.append({'id': entry['id'], 'title': entry.get('title', entry['id'])})
            return videos
    except json.JSONDecodeError:
        pass
    
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        try:
            data = json.loads(line)
            if 'id' in data:
                videos.append({'id': data['id'], 'title': data.get('title', data['id'])})
        except json.JSONDecodeError:
            pass
    return videos

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " ._-").strip()

def download_transcripts(playlist_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    videos = get_videos_from_playlist(playlist_url)
    if not videos:
        print("No videos found.")
        return

    api = YouTubeTranscriptApi()
    
    for video in videos:
        video_id = video['id']
        title = video['title']
        filename = sanitize_filename(title) + ".txt"
        filepath = os.path.join(output_dir, filename)
        
        if os.path.exists(filepath):
            print(f"Skipping {title} (already exists)")
            continue

        print(f"Fetching transcript for: {title} ({video_id})")
        
        try:
            data = api.fetch(video_id)
            formatted_transcript = "\n".join([snippet['text'] for snippet in data])
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_transcript)
            print(f"Saved to {filepath}")
            
        except Exception as e:
            print(f"Could not get transcript for {title}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download.py <playlist_url> [output_dir]")
        sys.exit(1)
        
    playlist_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "transcripts"
    
    download_transcripts(playlist_url, output_dir)
