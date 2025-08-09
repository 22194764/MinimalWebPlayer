# MinimalWebPlayer

MinimalWebPlayer is a zero-config, folder-based web app for watching your locally saved TV shows and anime, with automatic episode tracking, resume, and subtitle support. Just point it at your media folder and enjoy a clean, Netflix-like experience in your browser—no server setup, no database, no nonsense.

---

## Features

- **Instant Library:**  
  Browse all `.mp4` and `.mkv` files in your chosen folder and subfolders. Folders appear as collapsible dropdowns in the sidebar.

- **Episode Tracking:**  
  Automatically remembers watched episodes and your last position in each episode (resume support).

- **Subtitles:**  
  Loads `.srt` subtitles automatically (if present). Embedded subtitles can be extracted using the included tool.

- **Minimal Controls:**  
  - Next Episode  
  - Skip Opening (jumps 90 seconds)  
  - Watch from Beginning

- **No Installation Needed:**  
  Runs as a simple Python HTTP server. No database, no dependencies except Python and ffmpeg for optional processing.

---

## Quick Start

1. **Install Python 3**.
2. **Run the server:**
   ```sh
   python server.py
   ```
   - Choose your media folder when prompted.
   - Your browser will open automatically.

3. **Enjoy!**  
   - Episodes and folders appear in the sidebar.
   - Click to play, resume, or mark as watched.

---

## Advanced: Clean Up MKV Files

If your `.mkv` files have multiple audio/subtitle tracks, use the included `process_mkv.py` tool to:

- **Keep only Japanese audio** (or your preferred language)
- **Extract English subtitles** as `.srt` files for web playback

**How to use:**
1. Install [ffmpeg](https://ffmpeg.org/)
2. Edit the script to select your language for audio and subtitles. 
2. Run the script. 
```sh
python process_mkv.py
```
- Select your folder of `.mkv` files.
- Processed files and extracted subtitles will be saved in a `Processed` subfolder.

---

## Why Use This?

- **No cloud, no tracking, no ads.**
- **Works offline.**
- **Perfect for anime or TV show collections.**
- **Remembers your progress and watched episodes.**
- **Handles subfolders and organizes your library automatically.**

---

## Requirements

- Python 3.x
- [ffmpeg](https://ffmpeg.org/) (for `process_mkv.py`)
- `pymediainfo` Python package (`pip install pymediainfo`)

---

## Changelog

### v1.1
- Added **Skip Opening** button (jumps ahead by 1 minute 30 seconds).
- Added **Play from Beginning** button for quick restarts.
- **Subtitle support:** Automatically loads `.srt` files with matching episode names.
- **Watched episodes** are highlighted in green.
- **Currently watching** episodes are highlighted in yellow.
- **Subfolder support:** Episodes in subfolders now appear as collapsible folders in the sidebar.
- **Automatic resume:** Remembers your last watched position for each episode.
- **process_mkv.py**: Powerful tool to batch-remove all audio tracks except your chosen language and extract subtitles of your preferred language from `.mkv` files. Uses ffmpeg and pymediainfo.
- **No installation required:** Just run the server and select your media folder—no config, no database, no browser plugins.
- **Episode auto-advance:** Automatically plays the next episode when one finishes.

### v1
- Basic web-based player for local video files.
- Simple sidebar episode list.
- Optional batch file for quick server startup.

---
**Copyright © 2025 Avinash Kumaran. All rights reserved.**

This software is for personal use only.  
Copying, redistribution, or modification without explicit permission is prohibited.
---
