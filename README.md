# HLS Downloader

A small Python utility for downloading an **HLS (`.m3u8`) stream** with [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and remuxing it into a standard **MP4** file using FFmpeg.

This is useful when an HLS stream is made up of many `.ts` fragments and saving those fragments directly produces a file that only tolerant players can open.

> Use this tool only for media that you are authorized to access and download. It is not intended to bypass DRM, authentication, paywalls, or other access controls.

## Features

- Downloads HLS `.m3u8` playlists
- Automatically remuxes the result to MP4
- Uses FFmpeg to avoid malformed MPEG-TS-in-MP4 files
- Supports optional `Referer` and `Origin` HTTP headers
- Keeps URLs, IDs, cookies, tokens, and site-specific information out of the source code

## Requirements

- Python 3.10+
- `yt-dlp`
- FFmpeg available in your system `PATH`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hls-downloader.git
cd hls-downloader
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

If you use Git Bash:

```bash
source .venv/Scripts/activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install FFmpeg

Confirm that FFmpeg is available:

```bash
ffmpeg -version
```

If the command is not found, install FFmpeg using your operating system's package manager and make sure its `bin` directory is on your `PATH`.

Examples:

#### Windows

```bash
winget install --id Gyan.FFmpeg -e
```

#### macOS

```bash
brew install ffmpeg
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

## Usage

### Basic download

```bash
python hls_downloader.py "https://example.com/path/playlist.m3u8"
```

The default output is:

```text
video.mp4
```

### Choose the output filename

```bash
python hls_downloader.py \
  "https://example.com/path/playlist.m3u8" \
  -o "lecture.%(ext)s"
```

This produces a properly remuxed file such as:

```text
lecture.mp4
```

Using `%(ext)s` is recommended because it lets `yt-dlp` use the correct intermediate container before FFmpeg remuxes it to MP4.

### Add a Referer header

Some authorized streams require the same `Referer` header used by the web player:

```bash
python hls_downloader.py \
  "https://example.com/path/playlist.m3u8" \
  --referer "https://example.com/player/"
```

### Add Referer and Origin headers

```bash
python hls_downloader.py \
  "https://example.com/path/playlist.m3u8" \
  --referer "https://example.com/player/" \
  --origin "https://example.com"
```

## Finding the HLS playlist

If you are debugging a stream you are authorized to access:

1. Open the page in your browser.
2. Open Developer Tools.
3. Go to **Network**.
4. Start or reload the video.
5. Filter requests by:

```text
m3u8
```

6. Look for a request ending in `.m3u8`.
7. Copy the exact request URL.

Individual files ending in `.ts` are usually only media fragments, not the complete playlist.

Example fragment:

```text
media_123.ts
```

Example playlist:

```text
playlist.m3u8
```

Use the playlist URL with this tool.

## Why FFmpeg is required

HLS streams commonly contain MPEG-TS fragments. If those fragments are simply concatenated and saved with an `.mp4` extension, the file may technically still contain MPEG-TS data or malformed AAC timestamps.

That can lead to symptoms such as:

- video plays only in VLC
- Windows Media Player refuses to open it
- seeking does not work correctly
- duration is wrong
- audio timestamps are broken

This project lets `yt-dlp` download the stream and then uses FFmpeg to remux it into a normal MP4 container.

## Troubleshooting

### `No module named yt_dlp`

Install the dependency in the same Python environment:

```bash
python -m pip install -U yt-dlp
```

Then verify:

```bash
python -m yt_dlp --version
```

### `ffmpeg: command not found`

FFmpeg may be installed but missing from `PATH`.

Check:

```bash
ffmpeg -version
```

On Windows you can also try:

```bash
where.exe ffmpeg
```

If necessary, add the directory containing `ffmpeg.exe` to your system or shell `PATH`.

### The downloaded file only plays in VLC

Make sure FFmpeg is installed and use this project instead of naming the raw HLS output directly as `.mp4`.

The downloader uses:

```text
--remux-video mp4
```

so FFmpeg creates a proper MP4 container after the HLS download finishes.

### HTTP 403

A `403 Forbidden` response usually means the server requires additional authorization or request context.

If the stream is one you are authorized to download, first verify that:

- the `.m3u8` URL is current
- the stream works in your browser
- the correct `Referer` or `Origin` header is required

Do not commit cookies, login tokens, session IDs, authorization headers, or other credentials to GitHub.

### HTTP 404

A `404 Not Found` normally means the playlist URL is incorrect or expired.

Do not guess the playlist filename from a `.ts` fragment. Copy the actual `.m3u8` request from the browser's Network panel.

## Security

Never put any of the following directly in this repository:

```text
cookies
session IDs
JWTs
authorization tokens
personal email addresses
account usernames
private media IDs
private server URLs
```

If you accidentally commit a secret, removing it from the latest file is not enough because it may remain in Git history. Revoke or rotate the exposed credential and remove it from the repository history.

## Example

```bash
python hls_downloader.py \
  "https://media.example.com/video/playlist.m3u8" \
  -o "my_video.%(ext)s" \
  --referer "https://media.example.com/player/" \
  --origin "https://media.example.com"
```

## License

MIT
