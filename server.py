import os
import http.server
import socketserver
import json
from urllib.parse import unquote
import tkinter as tk
from tkinter import filedialog
import webbrowser
import threading

PORT = 8000

# GUI folder picker
root = tk.Tk()
root.withdraw()
media_folder = filedialog.askdirectory(title="Select your media folder")
if not media_folder:
    print("No folder selected, exiting.")
    exit(1)

def list_episodes():
    episode_files = []
    for root_dir, dirs, files in os.walk(media_folder):
        for f in files:
            if f.lower().endswith(('.mkv', '.mp4')):
                full_path = os.path.join(root_dir, f)
                rel_path = os.path.relpath(full_path, media_folder)
                episode_files.append(rel_path.replace("\\", "/"))
    return sorted(episode_files)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve episodes.json from script folder
        if self.path == '/episodes.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            eps = list_episodes()
            self.wfile.write(json.dumps(eps).encode())
            return

        # Serve index.html and other static files from script folder
        if self.path == '/' or self.path.startswith('/index.html'):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, 'index.html')
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404)
                return

        # Serve media files (video, srt) from media_folder
        filepath = unquote(self.path.lstrip('/'))
        full_path = os.path.join(media_folder, filepath)
        if os.path.isfile(full_path):
            try:
                file_size = os.path.getsize(full_path)
                range_header = self.headers.get('Range', None)
                # Serve SRT files as text/plain
                if full_path.endswith('.srt'):
                    with open(full_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain; charset=utf-8')
                        self.send_header("Content-Length", str(file_size))
                        self.end_headers()
                        self.wfile.write(f.read())
                    return
                if range_header:
                    start, end = 0, file_size - 1
                    m = range_header.replace('bytes=', '').split('-')
                    if m[0]:
                        start = int(m[0])
                    if len(m) > 1 and m[1]:
                        end = int(m[1])
                    if start > end or end >= file_size:
                        self.send_error(416, "Requested Range Not Satisfiable")
                        return
                    self.send_response(206)
                    self.send_header('Content-type', 'video/mp4' if full_path.endswith('.mp4') else 'video/x-matroska')
                    self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                    self.send_header('Content-Length', str(end - start + 1))
                    self.send_header('Accept-Ranges', 'bytes')
                    self.end_headers()
                    with open(full_path, 'rb') as f:
                        f.seek(start)
                        self.wfile.write(f.read(end - start + 1))
                    return
                else:
                    with open(full_path, 'rb') as f:
                        self.send_response(200)
                        if full_path.endswith('.mkv'):
                            self.send_header('Content-type', 'video/x-matroska')
                        elif full_path.endswith('.mp4'):
                            self.send_header('Content-type', 'video/mp4')
                        else:
                            self.send_header('Content-type', 'application/octet-stream')
                        self.send_header("Content-Length", str(file_size))
                        self.send_header('Accept-Ranges', 'bytes')
                        self.end_headers()
                        self.wfile.write(f.read())
                    return
            except Exception as e:
                print(f"Failed to serve file {full_path}: {e}")
                self.send_error(404)
                return

        # Fallback: serve other static files from script folder if needed
        script_dir = os.path.dirname(os.path.abspath(__file__))
        static_path = os.path.join(script_dir, self.path.lstrip('/'))
        if os.path.isfile(static_path):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.send_error(404)

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == "__main__":
    # Do NOT chdir to media_folder!
    threading.Thread(target=open_browser, daemon=True).start()
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        print(f"Media folder set to: {media_folder}")
        httpd.serve_forever()
