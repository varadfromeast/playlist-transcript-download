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
python download.py <playlist_url> [-o OUTPUT_DIR] [-l LANGUAGES [LANGUAGES ...]] [-c COOKIES]
```

### Options
- `playlist_url`: The URL of the YouTube playlist.
- `-o OUTPUT_DIR`, `--output_dir OUTPUT_DIR`: Output directory for the transcripts. Defaults to `transcripts`.
- `-l LANGUAGES`, `--languages LANGUAGES`: A list of language codes to download (e.g., `en`, `hi`, `es`). Defaults to `en`. If a language is not available for a given video, the script will skip downloading it.
- `-c COOKIES`, `--cookies COOKIES`: Path to a `cookies.txt` file (in Netscape format) to bypass IP blocks. You can export this file using browser extensions like 'Get cookies.txt LOCALLY'.

### Examples

Download the default English transcript to the `transcripts` folder:
```bash
python download.py "https://www.youtube.com/playlist?list=PLipQy8ycGNtRCGfpJbfrYRABQpIsJOapY"
```

Download both English and Hindi transcripts into a specific folder:
```bash
python download.py "https://www.youtube.com/playlist?list=PLipQy8ycGNtRCGfpJbfrYRABQpIsJOapY" -o my_transcripts -l en hi
```

This will download transcripts for all videos in the playlist as `.txt` files into the specified output folder. The filenames will have the language code appended (e.g., `Video_Title_en.txt`, `Video_Title_hi.txt`). If a transcript already exists, it will skip it.
