import os
import subprocess
from pymediainfo import MediaInfo

import tkinter as tk
from tkinter import filedialog

def pick_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select folder containing MKV files")
    root.destroy()
    return folder_selected

folder = pick_folder()
if not folder:
    print("No folder selected. Exiting.")
    exit(1)

output_folder = os.path.join(folder, 'Processed')
os.makedirs(output_folder, exist_ok=True)

def get_streams_info(filepath):
    media_info = MediaInfo.parse(filepath)
    audio_streams = []
    subtitle_streams = []
    audio_idx = 0
    subtitle_idx = 0
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            audio_streams.append({
                'index': audio_idx,
                'language': track.language
            })
            audio_idx += 1
        elif track.track_type == 'Text':
            subtitle_streams.append({
                'index': subtitle_idx,
                'language': track.language
            })
            subtitle_idx += 1
    return audio_streams, subtitle_streams

def process_file(filepath):
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    print(f"Processing {filename}...")

    audio_streams, subtitle_streams = get_streams_info(filepath)

    print("Detected audio languages:")
    for a in audio_streams:
        print(f"  Audio stream index {a['index']}: {a['language']}")

    print("Detected subtitle languages:")
    for s in subtitle_streams:
        print(f"  Subtitle stream index {s['index']}: {s['language']}")

    # Find Japanese audio index (first one)
    jpn_audio_idx = None
    for a in audio_streams:
        if a['language'] == 'ja' or a['language'] == 'jpn':
            jpn_audio_idx = a['index']
            break

    if jpn_audio_idx is None:
        print("No Japanese audio found, skipping.")
        return
    else:
        print(f"Selected audio language to keep: {audio_streams[jpn_audio_idx]['language']} (stream index {jpn_audio_idx})")

    # Find English subtitle index (first one)
    eng_sub_idx = None
    for s in subtitle_streams:
        if s['language'] == 'en' or s['language'] == 'eng':
            eng_sub_idx = s['index']
            break

    # Build stream mapping: keep all video, only Japanese audio, no subtitles
    # Use ffmpeg's stream specifiers: 0:v (all video), 0:a:<idx> (audio), 0:s:<idx> (subtitle)
    stream_maps = ['-map', '0:v']  # all video streams
    stream_maps += ['-map', f'0:a:{jpn_audio_idx}']  # only Japanese audio

    output_mkv = os.path.join(output_folder, filename)
    output_srt = os.path.join(output_folder, f"{name}.srt")

    # Copy only video and Japanese audio
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', filepath,
        *stream_maps,
        '-c', 'copy',
        output_mkv
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Saved processed video: {output_mkv}")

    # Extract English subtitles if present
    if eng_sub_idx is not None:
        ffmpeg_sub_cmd = [
            'ffmpeg', '-y', '-i', filepath,
            '-map', f'0:s:{eng_sub_idx}',
            output_srt
        ]
        subprocess.run(ffmpeg_sub_cmd, check=True)
        print(f"Extracted English subtitles: {output_srt}")
    else:
        print("No English subtitles found.")

def main():
    for file in os.listdir(folder):
        if file.lower().endswith('.mkv'):
            filepath = os.path.join(folder, file)
            try:
                process_file(filepath)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {file}: {e}")

if __name__ == '__main__':
    main()
