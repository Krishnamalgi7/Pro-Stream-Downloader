import streamlit as st
import os
import yt_dlp
import sys

# 1. DEFINE the function at the top
def get_ffmpeg_path():
    """Locates ffmpeg.exe inside the bundled EXE folder"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.getcwd()

# --- Configuration ---
BASE_FOLDER = "data"
SONGS_FOLDER = os.path.join(BASE_FOLDER, "songs")
VIDEOS_FOLDER = os.path.join(BASE_FOLDER, "videos")

os.makedirs(SONGS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

st.set_page_config(page_title="Pro Media Downloader", page_icon="🚀", layout="wide")

# --- TOP EXIT BUTTON ---
col_title, col_exit_top = st.columns([4, 1])
with col_exit_top:
    if st.button("🛑 Stop Server & Exit", use_container_width=True, type="primary", key="top_exit"):
        st.success("Stopping...")
        os._exit(0)
st.divider()


# --- Helper Functions ---
def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def format_bytes(size):
    if size is None: return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0


# --- Progress Bar Hook ---
def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%', '')
        try:
            percent_val = float(p) / 100
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            progress_bar.progress(percent_val)
            status_msg.info(f"Downloading: {p}% | Speed: {speed} | ETA: {eta}")
        except:
            pass
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_msg.success("Download complete! Finalizing file...")


# --- Main UI ---
st.title("🚀 Pro Media Downloader")

# --- DETAILS EXPANDER ---
with st.expander("📊 View Quality Details"):
    st.markdown("### ℹ️ Quality & Bitrate Reference Guide")
    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("**🎵 Audio (MP3) Bitrates**")
        st.table([
            {"Bitrate": "64 kbps", "Use Case": "Voice/Low Storage"},
            {"Bitrate": "128 kbps", "Use Case": "Standard Mobile"},
            {"Bitrate": "192 kbps", "Use Case": "Good Balance"},
            {"Bitrate": "256 kbps", "Use Case": "High Quality"},
            {"Bitrate": "320 kbps", "Use Case": "Ultra/Best Quality"}
        ])

    with t_col2:
        st.markdown("**🎥 Video (MP4) Resolutions**")
        st.table([
            {"Res": "144p", "Use Case": "Emergency Saver"},
            {"Res": "360p", "Use Case": "Small Screens"},
            {"Res": "480p", "Use Case": "Standard Definition"},
            {"Res": "720p", "Use Case": "HD Quality"},
            {"Res": "1080p", "Use Case": "Full HD (Sharp)"},
            {"Res": "1440p", "Use Case": "2K / QHD (Highest)"}
        ])

# --- Download Section ---
st.divider()
with st.container(border=True):
    col_url, col_type, col_qual = st.columns([2, 1, 1])

    with col_url:
        url = st.text_input(
            "🔗 Paste YouTube Link:",
            placeholder="Paste link and press Enter...",
            help="Press Enter after pasting to verify the video details."
        )

    with col_type:
        download_type = st.selectbox("📦 Format", ["Music (MP3)", "Video (MP4)"])

    with col_qual:
        if download_type == "Music (MP3)":
            bitrate = st.selectbox("🎧 Bitrate", ["64", "128", "192", "256", "320"], index=3)
            ydl_format = 'bestaudio/best'
        else:
            quality_choice = st.selectbox("📺 Resolution", ["144p", "360p", "480p", "720p", "1080p", "1440p"], index=4)
            height_map = {"144p": 144, "360p": 360, "480p": 480, "720p": 720, "1080p": 1080, "1440p": 1440}
            target_height = height_map[quality_choice]
            ydl_format = f'bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]'

    # --- Auto-fetch Metadata Logic ---
    if url:
        try:
            with yt_dlp.YoutubeDL({'format': ydl_format, 'quiet': True, 'noplaylist': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                st.info(f"✨ **Ready to Download:** {info.get('title')[:80]}...")

        except Exception as e:
            st.error("Unable to fetch video details. Check URL.")

    if st.button("🚀 Start Download", use_container_width=True):
        if not url:
            st.warning("Please enter a URL!")
        else:
            progress_bar = st.progress(0)
            status_msg = st.empty()

            # --- GET PORTABLE FFMPEG PATH ---
            ffmpeg_loc = get_ffmpeg_path()

            try:
                if download_type == "Music (MP3)":
                    opts = {
                        'format': 'bestaudio/best',
                        'ffmpeg_location': ffmpeg_loc,  # 👈 ADDS FFmpeg PATH
                        'outtmpl': f'{SONGS_FOLDER}/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [progress_hook],
                        'postprocessors': [
                            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate}],
                    }
                else:
                    opts = {
                        'format': ydl_format,
                        'ffmpeg_location': ffmpeg_loc,  # 👈 ADDS FFmpeg PATH
                        'outtmpl': f'{VIDEOS_FOLDER}/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'merge_output_format': 'mp4',
                        'progress_hooks': [progress_hook],
                    }
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# --- Library Section ---
st.divider()
st.header("📂 Local Library")
tab_music, tab_video = st.tabs(["🎵 Music", "🎥 Videos"])

# --- MUSIC TAB ---
with tab_music:
    files = [f for f in os.listdir(SONGS_FOLDER) if f.endswith('.mp3')]
    if files:
        for f in files:
            file_path = os.path.join(SONGS_FOLDER, f)
            try:
                # Calculate file size
                file_size = os.path.getsize(file_path)
                size_str = format_bytes(file_size)
            except:
                size_str = "Unknown"

            # Display size in the title
            with st.expander(f"🎶 {f}  [{size_str}]"):
                st.audio(file_path)
                if st.button(f"🗑️ Delete", key=f"del_{f}"):
                    os.remove(file_path)
                    st.rerun()
    else:
        st.info("Music folder is empty.")

# --- VIDEO TAB ---
with tab_video:
    v_files = [f for f in os.listdir(VIDEOS_FOLDER) if f.endswith('.mp4')]
    if v_files:
        for f in v_files:
            file_path = os.path.join(VIDEOS_FOLDER, f)
            try:
                # Calculate file size
                file_size = os.path.getsize(file_path)
                size_str = format_bytes(file_size)
            except:
                size_str = "Unknown"

            # Display size in the title
            with st.expander(f"🎬 {f}  [{size_str}]"):
                st.video(file_path)
                if st.button(f"🗑️ Delete", key=f"del_v_{f}"):
                    os.remove(file_path)
                    st.rerun()
    else:
        st.info("Video folder is empty.")

# --- Storage Indicator ---
st.divider()
total_storage = get_dir_size(BASE_FOLDER)
col_s1, col_s2 = st.columns([4, 1])
with col_s1:
    st.write(f"📊 **Total Library Storage Used:** {format_bytes(total_storage)}")
with col_s2:
    if st.button("🧹 Wipe All Data"):
        for folder in [SONGS_FOLDER, VIDEOS_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        st.rerun()

