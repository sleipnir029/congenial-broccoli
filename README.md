# congenial-broccoli

This project includes two separate scripts—one for **macOS** and one for **Windows**—that automate the process of capturing and recording YouTube videos from a **CSV file** by:
- Extracting metadata (title and duration).
- Modifying the video URL to disable autoplay and subtitles.
- Opening the video in a browser.
- Recording a specific screen region using **ffmpeg**.
- Closing the browser automatically.
- Saving the recording with a **sanitized filename**.

Additionally, all necessary dependencies are listed in **`requirements.txt`**.

---

### 📖 Table of Contents
- [congenial-broccoli](#congenial-broccoli)
    - [📖 Table of Contents](#-table-of-contents)
  - [📌 Requirements](#-requirements)
    - [🔹 Python Packages](#-python-packages)
    - [🔹 External Tools](#-external-tools)
    - [🛠 How the Script Works](#-how-the-script-works)
    - [📂 CSV File Format](#-csv-file-format)
    - [📺 Screen Capture Configuration](#-screen-capture-configuration)
      - [🔹 macOS (`mac_record.py`)](#-macos-mac_recordpy)
      - [🔹 Windows (win\_record.py)](#-windows-win_recordpy)
      - [🔹 macOS](#-macos)
      - [🔹 Windows](#-windows)
    - [⚠️ Notes \& Troubleshooting](#️-notes--troubleshooting)
    - [🎯 Summary](#-summary)
    - [📌 Conclusion](#-conclusion)

---

## 📌 Requirements

### 🔹 Python Packages
Install the required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt



---

## 📌 Requirements

### 🔹 Python Packages
Install the required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

**Note:** The dependencies include:

- yt-dlp for extracting video metadata.
- pyautogui for browser control (Windows only).
- opencv-python, mss, and numpy for screen capturing.

### 🔹 External Tools
**macOS:**
- ffmpeg (Required for screen capture):
```bash
brew install ffmpeg
```
- Verify Available Screens for Capture:
```bash
ffmpeg -f avfoundation -list_devices true -i ""
```
This command will list all available screens and audio devices. Set `video_device` in `mac_record.py` accordingly.

**Windows:**
- ffmpeg (Download from ffmpeg.org and add it to your PATH).
- Verify Available Screens for Capture:
```bash
ffmpeg -list_devices true -f dshow -i dummy
```
This command will list `available capture devices` for Windows.

---

### 🛠 How the Script Works
> CSV to Recording Workflow
1. **CSV Input:** The script reads YouTube links from `videos.csv`.
2. **Video Metadata Extraction:** Uses `yt-dlp` to get title and duration.
3. **URL Modification:** Disables autoplay and subtitles. [Doesn't work - couldn't get a way around it 💁]
4. **Open in Browser:** The default browser loads the video.
5. **Wait:** A 1-second delay allows loading.
6. **Screen Recording:** Captures a specified region for the video duration.
7. **Browser Closure:**
    - **macOS:** Uses AppleScript.
    - **Windows:** Uses pyautogui (`Ctrl+W` & `Alt+F4`).
8. **File Saving:** The recorded file is saved with a sanitized filename.

---

### 📂 CSV File Format
The script expects a **CSV file** (`videos.csv`) with one **YouTube URL** per line:

```bash
https://www.youtube.com/watch?v=example1
https://www.youtube.com/watch?v=example2
```

---

### 📺 Screen Capture Configuration
The screen region to capture is customizable in both scripts:

#### 🔹 macOS (`mac_record.py`)
Modify `region` in the script:

```python
region = {"left": 50, "top": 300, "width": 1900, "height": 1200}
```
- `left`: X position (starting point)
- `top`: Y position (starting point)
- `width`: Width of the capture area
- `height`: Height of the capture area

> Ensure the correct `video_device` value is set (Check with `ffmpeg -f avfoundation -list_devices true -i ""`).

#### 🔹 Windows (win_record.py)
Modify `region` in the script:

```python
region = {"left": 100, "top": 100, "width": 800, "height": 600}
```
- `offset_x` → `left`
- `offset_y` → `top`
- `video_size` → `width x height`

> Ensure ffmpeg is in the PATH and the correct device is used.

---

▶️ Running the Scripts
#### 🔹 macOS
```bash
python mac_record.py
```
#### 🔹 Windows
```bash
python win_record.py
```

### ⚠️ Notes & Troubleshooting
- Ensure ffmpeg is installed and configured properly.
- Adjust the capture region (`region` dictionary) based on your screen setup.
- On macOS, verify available screens using `ffmpeg -f avfoundation -list_devices true -i ""`.
- On Windows, check `ffmpeg -list_devices true -f dshow -i dummy` for screen input sources.
- On Windows, `pyautogui` requires administrative permissions for simulating keypresses.


### 🎯 Summary
|Feature	|macOS (mac_record.py)	|Windows (win_record.py)|
|-----------|-----------------------|-----------------------|
|YouTube Metadata Extraction	|✅ yt-dlp	|✅ yt-dlp|
|URL Modification (Disable Autoplay/Subtitles)	|✅	|✅|
|Opens Video in Native Browser	|✅|	✅|
|Waits Before Recording	|✅ (1s)	|✅ (1s)|
|Records Screen Region	|✅ avfoundation|✅ gdigrab|
|Closes Browser	|✅ AppleScript	|✅ pyautogui (Ctrl+W, Alt+F4)|
|Saves Recording	|✅ .mp4 file	|✅ .mp4 file|

---

### 📌 Conclusion
This script automates YouTube video screen recording by fetching video metadata, setting up a recording session, and automatically closing the browser once the recording is complete. Users can modify the capture region and adjust ffmpeg settings for their specific use case.



