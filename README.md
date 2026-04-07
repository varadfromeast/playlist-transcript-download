# Playlist Transcript Download

A simple Python script to download YouTube video transcripts from an entire playlist.

## Prerequisites

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python download.py <playlist_url> [output_directory]
```

### Example
```bash
python download.py "https://www.youtube.com/playlist?list=PLipQy8ycGNtRCGfpJbfrYRABQpIsJOapY" transcripts
```

This will download transcripts for all videos in the playlist as `.txt` files into the `transcripts` folder. If a transcript already exists, it will skip it.
