import subprocess
import sys

# ============================================================
# CONFIGURATION — CHANGE THESE IF NECESSARY
# ============================================================

# Main streaming server you found in DevTools
STREAM_BASE = "https://stream.library.utoronto.ca:1935"

# Media path
APP_PATH = "MyMedia/play"

# Video/media ID found in your requests
MEDIA_ID = "ee7a9e15f1e45d734ea0c166efc856c0"

# Rendition/stream IDs seen in your .ts requests
#
# Most recent one:
RENDITION_ID = "1392460422"
#
# Another one you saw earlier:
# RENDITION_ID = "151093730"


# Example segment numbers you saw:
SEGMENT_NUMBER = 4

# Example .ts URL.
# This is NOT the whole video — just one segment.
TS_URL = (
    f"{STREAM_BASE}/{APP_PATH}/mp4:1/{MEDIA_ID}.mp4/"
    f"media_w{RENDITION_ID}_{SEGMENT_NUMBER}.ts"
)

# Website/player origin you found
PLAYER_ORIGIN = "https://play.library.utoronto.ca"

# API endpoint you found.
# This is NOT the video URL and normally is NOT needed for downloading.
GRAPHQL_URL = "https://mymedia-api.library.utoronto.ca/graphql"


# ------------------------------------------------------------
# IMPORTANT:
#
# You still need the actual .m3u8 URL from:
#
# Chrome -> F12 -> Network -> filter: m3u8
#
# Right click the .m3u8 request:
# Copy -> Copy URL
#
# Paste it below.
# ------------------------------------------------------------

M3U8_URL = "https://stream.library.utoronto.ca:1935/MyMedia/play/mp4:1/ee7a9e15f1e45d734ea0c166efc856c0.mp4/playlist.m3u8"

# Example:
#
# M3U8_URL = "https://stream.library.utoronto.ca:1935/.....m3u8"
#
# Do NOT simply replace .ts with .m3u8 unless DevTools shows that URL.


# Optional: URL of the page where you watch the video.
#
# This can sometimes be used directly with yt-dlp together with
# --cookies-from-browser chrome.
#
VIDEO_PAGE_URL = ""

# Example:
# VIDEO_PAGE_URL = "https://play.library.utoronto.ca/........"


# Output filename
OUTPUT_FILE = "video.mp4"


# ============================================================
# SHOW THE CURRENT VALUES
# ============================================================

print("=" * 70)
print("CURRENT CONFIGURATION")
print("=" * 70)

print("Stream base:      ", STREAM_BASE)
print("Media ID:         ", MEDIA_ID)
print("Rendition ID:     ", RENDITION_ID)
print("Example TS URL:   ", TS_URL)
print("Player origin:    ", PLAYER_ORIGIN)
print("GraphQL API:      ", GRAPHQL_URL)

print("=" * 70)


# ============================================================
# DOWNLOAD METHOD 1 — yt-dlp using the .m3u8 URL
# ============================================================

def download_m3u8():
    import subprocess
    import sys

    M3U8_URL = (
        "https://stream.library.utoronto.ca:1935/"
        "MyMedia/play/mp4:1/"
        "ee7a9e15f1e45d734ea0c166efc856c0.mp4/"
        "playlist.m3u8"
    )

    PLAYER_ORIGIN = "https://play.library.utoronto.ca"
    OUTPUT_FILE = "video.mp4"

    command = [
        sys.executable,
        "-m",
        "yt_dlp",

        "--add-header",
        f"Referer:{PLAYER_ORIGIN}/",

        "--add-header",
        f"Origin:{PLAYER_ORIGIN}",

        "-o",
        OUTPUT_FILE,

        M3U8_URL,
    ]

    print("\nRunning:")
    print(" ".join(command))

    subprocess.run(command, check=True)

    return True


# ============================================================
# DOWNLOAD METHOD 2 — try the actual video webpage
# ============================================================

def download_from_page():
    """
    Lets yt-dlp inspect the video webpage itself.

    This may work if yt-dlp supports the site/player.
    """

    if not VIDEO_PAGE_URL:
        print("\nERROR: VIDEO_PAGE_URL is empty.")
        return False

    command = [
        sys.executable,
        "-m",
        "yt_dlp",

        "--cookies-from-browser",
        "chrome",

        "-o",
        "video.%(ext)s",

        VIDEO_PAGE_URL,
    ]

    print("\nRunning:")
    print(" ".join(command))

    subprocess.run(command, check=True)

    return True


# ============================================================
# DOWNLOAD METHOD 3 — ffmpeg from known .m3u8
# ============================================================

def download_with_ffmpeg():
    """
    Alternative to yt-dlp.

    Requires ffmpeg to be installed and available in PATH.
    """

    if not M3U8_URL:
        print("\nERROR: M3U8_URL is empty.")
        return False

    command = [
        "ffmpeg",

        "-headers",
        (
            f"Referer: {PLAYER_ORIGIN}/\r\n"
            f"Origin: {PLAYER_ORIGIN}\r\n"
        ),

        "-i",
        M3U8_URL,

        "-c",
        "copy",

        "-bsf:a",
        "aac_adtstoasc",

        OUTPUT_FILE,
    ]

    print("\nRunning ffmpeg...")

    subprocess.run(command, check=True)

    return True


# ============================================================
# MAIN
# ============================================================

print("""
Choose what you want to do:

1 = Download using M3U8_URL with yt-dlp
2 = Try downloading from VIDEO_PAGE_URL using Chrome cookies
3 = Download M3U8_URL using ffmpeg
4 = Just print URLs / configuration
""")

choice = input("Enter 1, 2, 3, or 4: ").strip()


if choice == "1":
    download_m3u8()

elif choice == "2":
    download_from_page()

elif choice == "3":
    download_with_ffmpeg()

elif choice == "4":
    print("\nNothing downloaded.")

else:
    print("Unknown option.")