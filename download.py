import os
import argparse
import json
import subprocess
import requests
import http.cookiejar
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

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

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " ._-").strip()

def download_transcripts(playlist_url, output_dir, languages, cookies_file=None):
    os.makedirs(output_dir, exist_ok=True)
    videos = get_videos_from_playlist(playlist_url)
    if not videos:
        print("No videos found.")
        return

    # Setup the YouTubeTranscriptApi with cookies if provided
    http_client = requests.Session()
    if cookies_file:
        if os.path.exists(cookies_file):
            print(f"Loading cookies from {cookies_file}...")
            cookie_jar = http.cookiejar.MozillaCookieJar(cookies_file)
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            http_client.cookies = cookie_jar
        else:
            print(f"Cookie file '{cookies_file}' not found. Ignoring cookies.")
    
    api = YouTubeTranscriptApi(http_client=http_client)

    for video in videos:
        video_id = video['id']
        title = video['title']
        
        print(f"Processing video: {title} ({video_id})")
        
        try:
            transcript_list = api.list(video_id)
        except TranscriptsDisabled:
            print(f"Transcripts are disabled for video {title}")
            continue
        except Exception as e:
            print(f"Could not retrieve transcripts for {title}: {e}")
            continue

        for lang in languages:
            filename = sanitize_filename(title) + f"_{lang}.txt"
            filepath = os.path.join(output_dir, filename)
            
            if os.path.exists(filepath):
                print(f"Skipping {lang} transcript for {title} (already exists)")
                continue

            try:
                # Check if the requested language is available (either manually created or generated)
                transcript = transcript_list.find_transcript([lang])
                data = transcript.fetch()
                
                formatted_lines = []
                for snippet in data:
                    start_time = format_timestamp(snippet['start'])
                    formatted_lines.append(f"[{start_time}] {snippet['text']}")
                    
                formatted_transcript = "\n".join(formatted_lines)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(formatted_transcript)
                print(f"Saved {lang} transcript to {filepath}")
                
            except NoTranscriptFound:
                print(f"Transcript in language '{lang}' not found for {title}. Skipping.")
            except Exception as e:
                print(f"Error fetching {lang} transcript for {title}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube playlist transcripts.")
    parser.add_argument("playlist_url", help="URL of the YouTube playlist")
    parser.add_argument("--output_dir", "-o", default="transcripts", help="Output directory for transcripts")
    parser.add_argument("--languages", "-l", nargs="+", default=["en"], help="Language codes to download (e.g. en hi es). Defaults to 'en'.")
    parser.add_argument("--cookies", "-c", help="Path to a Netscape formatted cookies.txt file to bypass IP blocks.")
    
    args = parser.parse_args()
    
    download_transcripts(args.playlist_url, args.output_dir, args.languages, args.cookies)
