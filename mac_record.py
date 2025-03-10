import csv
import urllib.parse
import webbrowser
import subprocess
import time
from yt_dlp import YoutubeDL

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

def record_screen_mac(region, duration, output_filename, fps=30, video_device="2", audio_device="none"):
    """
    Records a specified screen region on macOS using ffmpeg (avfoundation).
    """
    # Build the crop filter: crop=width:height:x:y
    crop_filter = f"crop={region['width']}:{region['height']}:{region['left']}:{region['top']}"
    
    if audio_device.lower() == "none":
        input_device = f"{video_device}:none"
    else:
        input_device = f"{video_device}:{audio_device}"
    
    command = [
        "ffmpeg",
        "-f", "avfoundation",
        "-framerate", str(fps),
        "-i", input_device,
        "-vf", crop_filter,
        "-t", str(duration),
        "-c:v", "libx264",
        output_filename
    ]
    
    print("Starting screen recording on macOS...")
    subprocess.run(command)
    print("Recording finished on macOS.")

def close_browser_macos():
    """
    Closes the frontmost browser window using AppleScript.
    Works with Safari or Google Chrome.
    """
    try:
        # Determine which app is frontmost
        result = subprocess.run(
            ['osascript', '-e', 'tell application "System Events" to get name of first process whose frontmost is true'],
            capture_output=True, text=True, check=True
        )
        app_name = result.stdout.strip()
        print(f"Frontmost application: {app_name}")
        
        if app_name == "Google Chrome":
            subprocess.run(['osascript', '-e', 'tell application "Google Chrome" to close front window'])
        elif app_name == "Safari":
            subprocess.run(['osascript', '-e', 'tell application "Safari" to close front document'])
        else:
            print(f"Frontmost app is {app_name}; not recognized for auto-closing.")
    except Exception as e:
        print("Error closing browser on macOS:", e)

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
                record_screen_mac(region, duration, output_filename, fps)
                
                # Wait 1 second for processing
                time.sleep(1)
                
                # Close the browser
                close_browser_macos()
                
                # Pause before next video
                time.sleep(2)
            except Exception as e:
                print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    # Adjust the capture region as needed
    region = {"left": 50, "top": 300, "width": 1900, "height": 1200}
    process_videos("videos.csv", region)
