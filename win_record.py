import csv
import urllib.parse
import webbrowser
import subprocess
import time
import sys
from yt_dlp import YoutubeDL
import pyautogui

def modify_url(url):
    """
    Modify the YouTube URL to disable autoplay and subtitles.
    """
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    query['autoplay'] = ['0']           # Disable autoplay
    query['cc_load_policy'] = ['0']     # Disable subtitles
    new_query = urllib.parse.urlencode(query, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_query))

def sanitize_filename(filename):
    """
    Remove characters not allowed in filenames.
    """
    return "".join(c for c in filename if c not in r'\/:*?"<>|')

def record_screen_windows(region, duration, output_filename, fps=30):
    """
    Records a specified screen region on Windows using ffmpeg (gdigrab).
    """
    video_size = f"{region['width']}x{region['height']}"
    command = [
        "ffmpeg",
        "-f", "gdigrab",
        "-framerate", str(fps),
        "-offset_x", str(region['left']),
        "-offset_y", str(region['top']),
        "-video_size", video_size,
        "-t", str(duration),
        "-i", "desktop",
        "-c:v", "libx264",
        output_filename
    ]
    print("Starting screen recording on Windows...")
    subprocess.run(command)
    print("Recording finished on Windows.")

def close_browser_windows():
    """
    Uses pyautogui to close the active browser tab/window on Windows.
    Tries Ctrl+W first, then Alt+F4 if needed.
    """
    time.sleep(0.5)  # Give the browser a moment to focus
    print("Attempting to close browser with Ctrl+W...")
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)
    print("Attempting to close browser with Alt+F4...")
    pyautogui.hotkey('alt', 'f4')

def process_videos(csv_filename, region, fps=30):
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            url = row[0].strip()
            if not url:
                continue
            try:
                # Extract video info using yt-dlp
                ydl_opts = {'quiet': True, 'skip_download': True}
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown_Title')
                duration = info.get('duration', 0)  # in seconds

                sanitized_title = sanitize_filename(title)
                output_filename = f"{sanitized_title}.mp4"
                
                print(f"\nProcessing Video: {title}")
                print(f"Duration: {duration} seconds")
                
                # Modify URL to disable autoplay & subtitles
                modified_url = modify_url(url)
                webbrowser.open(modified_url)
                
                # Wait 1 second for the video to load
                time.sleep(1)
                
                # Record screen for the video's duration
                record_screen_windows(region, duration, output_filename, fps)
                
                # Wait 1 second for processing
                time.sleep(1)
                
                # Close the browser
                close_browser_windows()
                
                # Pause before next video
                time.sleep(2)
            except Exception as e:
                print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    # Adjust the capture region as needed
    region = {"left": 100, "top": 100, "width": 800, "height": 600}
    process_videos("videos.csv", region)
