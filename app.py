import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import threading
import time
import yt_dlp

# --- 1. SETUP & HELPER FUNCTIONS ---
def get_ffmpeg_path():
    """Locates ffmpeg.exe inside the bundled EXE folder"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.getcwd()

def load_asset(file_path):
    """Reads external files (CSS, JS, HTML) from the assets folder. Handles PyInstaller paths."""
    base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd()
    full_path = os.path.join(base_path, file_path)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"⚠️ Error: Could not find {file_path}. Ensure it exists in the 'assets' folder.")
        return ""


# --- Configuration ---
BASE_FOLDER = "data"
SONGS_FOLDER = os.path.join(BASE_FOLDER, "songs")
VIDEOS_FOLDER = os.path.join(BASE_FOLDER, "videos")

os.makedirs(SONGS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="Pro Media Downloader",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LOAD & INJECT ASSETS ---
# Load CSS
css_code = load_asset(os.path.join("assets", "style.css"))
if css_code:
    st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

# Load JavaScript
js_code = load_asset(os.path.join("assets", "script.js"))
if js_code:
    st.markdown(f"<script>{js_code}</script>", unsafe_allow_html=True)


# --- 3. CORE LOGIC (Helpers) ---
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


def check_duplicate(title, dl_type):
    folder = SONGS_FOLDER if dl_type == "Music (MP3)" else VIDEOS_FOLDER
    import re
    def normalize(t):
        t = re.sub(r'[^\w\s]', '', t, flags=re.UNICODE)
        return re.sub(r'\s+', ' ', t).strip().lower()

    normalized_title = normalize(title)

    if not os.path.exists(folder):
        return None

    for existing in os.listdir(folder):
        name_no_ext = os.path.splitext(existing)[0]
        if normalize(name_no_ext) == normalized_title:
            return os.path.join(folder, existing)
    return None


# --- 4. DOWNLOAD LOGIC ---
def perform_download(url, opts, target_folder):
    st.info("⏳ Download in Progress kindly wait until download completes..........")
    progress_bar = st.progress(0)
    status_msg = st.empty()

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%', '')
            try:
                percent_val = float(p) / 100
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                progress_bar.progress(percent_val)
                status_msg.info(f"⚡ Downloading: **{p}%** | Speed: **{speed}** | ETA: **{eta}**")
            except:
                pass
        elif d['status'] == 'finished':
            progress_bar.progress(1.0)
            status_msg.success("✅ Download complete! Finalizing file...")

    opts['progress_hooks'] = [progress_hook]

    try:
        opts['overwrites'] = True
        opts['force_overwrites'] = True
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        st.toast("✅ Download Completed Successfully!", icon="🎉")
        st.session_state.download_done = True
        st.session_state.download_error = None
        st.session_state.last_url = ''
        st.session_state.fetched_title = None
        st.session_state.dup = None
        st.session_state.download_done = False
        time.sleep(1)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")


# --- 5. UI COMPONENTS ---
@st.dialog("⚠️ File Already Exists")
def confirm_overwrite_dialog(file_path, url, opts, target_folder):
    st.warning(f"The file **{os.path.basename(file_path)}** already exists in your library.")
    st.write("Do you want to download it again? This will overwrite the existing file.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, Overwrite", type="primary", use_container_width=True):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                st.session_state['trigger_download'] = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
    with col2:
        if st.button("❌ No, Cancel", type="secondary", use_container_width=True):
            st.rerun()


# Header
st.markdown("""
<div style="position: fixed; top: 10px; left: 20px; z-index: 999; background: rgba(21, 27, 59, 0.8); 
            backdrop-filter: blur(10px); padding: 8px 16px; border-radius: 8px; 
            border: 1px solid rgba(0, 212, 255, 0.3);">
    <span style="color: #8B9DC3; font-size: 12px; font-weight: 500;">
        👨‍💻 Developed by: <span style="color: #00D4FF; font-weight: 600;">Krishna Malgi</span>
    </span>
</div>
""", unsafe_allow_html=True)

header_col1, header_col2 = st.columns([6, 1])
with header_col1:
    st.markdown('<div style="padding: 10px 0;"><span class="logo-text"> Pro Media Downloader</span></div>',
                unsafe_allow_html=True)
with header_col2:
    if st.button("🔴 Exit ", key="top_exit", type="secondary"):
        st.success("Stopping server...")
        os._exit(0)

st.markdown("---")

# Details Expander
with st.expander("📊 Quality & Bitrate Reference Guide"):
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown("#### 🎵 Audio (MP3) Bitrates")
        st.table([{"Bitrate": "64 kbps", "Use Case": "Voice/Low Storage"},
                  {"Bitrate": "128 kbps", "Use Case": "Standard Mobile"},
                  {"Bitrate": "192 kbps", "Use Case": "Good Balance"},
                  {"Bitrate": "256 kbps", "Use Case": "High Quality"},
                  {"Bitrate": "320 kbps", "Use Case": "Ultra/Best Quality"}])
    with t_col2:
        st.markdown("#### 🎥 Video (MP4) Resolutions")
        st.table([{"Res": "144p", "Use Case": "Emergency Saver"},
                  {"Res": "360p", "Use Case": "Small Screens"},
                  {"Res": "480p", "Use Case": "Standard Definition"},
                  {"Res": "720p", "Use Case": "HD Quality"},
                  {"Res": "1080p", "Use Case": "Full HD (Sharp)"},
                  {"Res": "1440p", "Use Case": "2K / QHD (Highest)"},
                  {"Res": "2160p", "Use Case": "4K / Ultra HD"},
                  {"Res": "4320p", "Use Case": "8K / Full Ultra HD"}])

st.markdown("---")

# --- 6. USER INPUTS ---
st.markdown("### 🎯 <span style='color: #FFFFFF; text-shadow: 0 0 10px rgba(0,212,255,0.5);'>Download Media</span>",
            unsafe_allow_html=True)

col_url, col_type, col_qual = st.columns([2, 1, 1])
with col_url:
    url = st.text_input("🔗 YouTube URL", placeholder="Paste your YouTube link here...", label_visibility="collapsed")
with col_type:
    download_type = st.selectbox("📦 Format", ["Music (MP3)", "Video (MP4)"], label_visibility="collapsed")
with col_qual:
    if download_type == "Music (MP3)":
        bitrate = st.selectbox("🎧 Quality", ["64", "128", "192", "256", "320"], index=3, label_visibility="collapsed")
        ydl_format = 'bestaudio/best'
    else:
        quality_choice = st.selectbox("📺 Quality", ["144p", "360p", "480p", "720p", "1080p", "1440p", "2160p (4K)", "4320p (8K)"], index=4,
                                      label_visibility="collapsed")
        height_map = {"144p": 144, "360p": 360, "480p": 480, "720p": 720, "1080p": 1080, "1440p": 1440,"2160p (4K)": 2160, "4320p (8K)": 4320}
        target_height = height_map[quality_choice]
        ydl_format = f'bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]'

# Session State
if 'last_url' not in st.session_state: st.session_state.last_url = ''
if 'fetched_title' not in st.session_state: st.session_state.fetched_title = None
if 'dup' not in st.session_state: st.session_state.dup = None
if 'download_done' not in st.session_state: st.session_state.download_done = False
if 'download_error' not in st.session_state: st.session_state.download_error = None
if 'trigger_download' not in st.session_state: st.session_state.trigger_download = False

# Auto-fetch Metadata
if url and (url != st.session_state.get('last_url', '') or download_type != st.session_state.get('last_type', '')):
    st.session_state.last_url = url
    st.session_state.last_type = download_type
    st.session_state.fetched_title = None
    st.session_state.dup = None
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            st.session_state.fetched_title = info.get('title', '')
            st.session_state.dup = check_duplicate(st.session_state.fetched_title, download_type)
    except:
        st.error("⚠️ Unable to fetch video details. Please check the URL.")

if st.session_state.get('fetched_title'):
    if st.session_state.get('dup'):
        dup_size = format_bytes(os.path.getsize(st.session_state.dup)) if os.path.exists(
            st.session_state.dup) else "Unknown"
        st.warning(f"⚠️ **File Already Exists!** — `{os.path.basename(st.session_state.dup)}` ({dup_size})")
    else:
        st.info(f"✨ **Ready to Download:** {st.session_state.fetched_title[:80]}...")

# Prepare Opts
ffmpeg_loc = get_ffmpeg_path()
target_folder = SONGS_FOLDER if download_type == "Music (MP3)" else VIDEOS_FOLDER

if download_type == "Music (MP3)":
    opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_loc,
        'outtmpl': f'{SONGS_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate}],
    }
else:
    opts = {
        'format': ydl_format,
        'ffmpeg_location': ffmpeg_loc,
        'outtmpl': f'{VIDEOS_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
    }

# Handle Trigger
if st.session_state.get('trigger_download'):
    st.session_state.trigger_download = False
    perform_download(url, opts, target_folder)

# Download Button
if st.button("🚀 Start Download", use_container_width=True):
    if not url:
        st.warning("⚠️ Please enter a URL!")
    else:
        title_check = st.session_state.get('fetched_title')
        if not title_check:
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title_check = info.get('title', '')
            except:
                pass

        existing_file = check_duplicate(title_check, download_type) if title_check else None

        if existing_file:
            confirm_overwrite_dialog(existing_file, url, opts, target_folder)
        else:
            perform_download(url, opts, target_folder)

# --- 7. LIBRARY & STORAGE ---
st.markdown("---")
st.markdown("### 📚 <span style='color: #FFFFFF; text-shadow: 0 0 10px rgba(0,212,255,0.5);'>Your Library</span>",
            unsafe_allow_html=True)
tab_music, tab_video = st.tabs(["🎵 Music Collection", "🎥 Video Collection"])

with tab_music:
    files = [f for f in os.listdir(SONGS_FOLDER) if f.endswith('.mp3')]
    if files:
        for f in files:
            file_path = os.path.join(SONGS_FOLDER, f)
            size_str = format_bytes(os.path.getsize(file_path)) if os.path.exists(file_path) else "Unknown"
            with st.expander(f"🎶 **{f}**"):
                st.markdown(f'<span class="badge badge-mp3">MP3</span><span class="badge badge-size">{size_str}</span>',
                            unsafe_allow_html=True)
                st.audio(file_path)
                if st.button(f"🗑️ Delete", key=f"del_{f}"):
                    os.remove(file_path)
                    st.rerun()
    else:
        st.info("🎵 Your music library is empty.")

with tab_video:
    v_files = [f for f in os.listdir(VIDEOS_FOLDER) if f.endswith('.mp4')]
    if v_files:
        for f in v_files:
            file_path = os.path.join(VIDEOS_FOLDER, f)
            size_str = format_bytes(os.path.getsize(file_path)) if os.path.exists(file_path) else "Unknown"
            with st.expander(f"🎬 **{f}**"):
                st.markdown(f'<span class="badge badge-mp4">MP4</span><span class="badge badge-size">{size_str}</span>',
                            unsafe_allow_html=True)
                st.video(file_path)
                if st.button(f"🗑️ Delete", key=f"del_v_{f}"):
                    os.remove(file_path)
                    st.rerun()
    else:
        st.info("🎥 Your video library is empty.")

st.markdown("---")
total_storage = get_dir_size(BASE_FOLDER)
col_s1, col_s2 = st.columns([4, 1])
with col_s1:
    st.markdown(
        f"### 📊 <span style='color: #FFFFFF; text-shadow: 0 0 10px rgba(0,212,255,0.5);'>Total Storage: **{format_bytes(total_storage)}**</span>",
        unsafe_allow_html=True)
with col_s2:
    if st.button("🧹 Clear All"):
        for folder in [SONGS_FOLDER, VIDEOS_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        st.rerun()

# --- 8. FOOTER INJECTION ---
st.markdown("---")
footer_code = load_asset(os.path.join("assets", "footer.html"))
if footer_code:
    components.html(footer_code, height=300)