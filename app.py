import streamlit as st
import streamlit.components.v1 as components
import os
import yt_dlp
import sys
import threading
import time


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

st.set_page_config(
    page_title="Pro Media Downloader",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR MODERN DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0F1535 0%, #1A2347 100%);
        color: #FFFFFF;
    }

    .logo-text {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF !important;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.6), 0 0 10px rgba(0, 212, 255, 0.8);
    }

    .logo-text::before {
        content: "🚀 ";
    }

    /* FIX FOR POPUP DIALOGS (Make them dark) */
    div[role="dialog"] {
        background: #1A2347 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* FIX FOR TOAST NOTIFICATIONS */
    div[data-testid="stToast"] {
        background-color: #1A2347 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Force text inside toast to be white */
    div[data-testid="stToast"] p, 
    div[data-testid="stToast"] div {
        color: #FFFFFF !important;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background: rgba(30, 39, 73, 0.6) !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        font-size: 16px !important;
        color: #FFFFFF !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #00D4FF !important;
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.3),
            0 0 0 4px rgba(0, 212, 255, 0.2),
            0 0 20px rgba(0, 212, 255, 0.4) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #4A5578 !important;
    }

    /* Select Box Styling */
    .stSelectbox > div > div {
        background: rgba(30, 39, 73, 0.9) !important;
        border: 1px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        transition: all 0.3s ease !important;
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(0, 212, 255, 0.7) !important;
        background: rgba(30, 39, 73, 1) !important;
    }

    /* Selected value text in selectbox */
    .stSelectbox [data-baseweb="select"] span {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    .stSelectbox [data-baseweb="select"] div {
        color: #FFFFFF !important;
    }

    /* Dropdown options menu container */
    .stSelectbox [data-baseweb="select"] > div {
        background: #1A2347 !important;
        color: #FFFFFF !important;
    }

    /* Dropdown Styling - Matching app background */
    [data-baseweb="popover"] {
        z-index: 999999 !important;
    }

    [data-baseweb="popover"] [data-baseweb="menu"] {
        background-color: #1A2347 !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.8) !important;
    }

    [data-baseweb="menu"] ul {
        background-color: #1A2347 !important;
        padding: 8px !important;
    }

    [data-baseweb="menu"] li {
        background-color: transparent !important;
        color: #FFFFFF !important;
        padding: 14px 18px !important;
        margin: 3px 0 !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        border: 1px solid transparent !important;
    }

    [data-baseweb="menu"] li:hover {
        background-color: rgba(30, 39, 73, 0.8) !important;
        color: #FFFFFF !important;
        border-color: rgba(0, 212, 255, 0.5) !important;
    }

    [data-baseweb="menu"] li[aria-selected="true"] {
        background-color: rgba(0, 212, 255, 0.25) !important;
        color: #00D4FF !important;
        font-weight: 600 !important;
        border-color: rgba(0, 212, 255, 0.6) !important;
    }

    /* Force dropdown to open DOWNWARD */
    .stSelectbox [data-baseweb="popover"] {
        position: absolute !important;
        top: 100% !important;
        bottom: auto !important;
        transform: none !important;
    }

    /* Force white text in dropdown options */
    [data-baseweb="menu"] li *,
    [role="option"] span,
    [role="option"] div {
        color: inherit !important;
    }

    /* Dropdown popover transparency */
    [data-baseweb="popover"] {
        background: transparent !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF 0%, #B537F2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3) !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Exit Button Styling - Override for secondary type */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 46, 99, 0.15) !important;
        border: 1px solid rgba(255, 46, 99, 0.5) !important;
        color: #FF4D7D !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
        box-shadow: 0 4px 15px rgba(255, 46, 99, 0.2) !important;
        width: auto !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 46, 99, 0.25) !important;
        border-color: #FF2E63 !important;
        box-shadow: 0 6px 20px rgba(255, 46, 99, 0.4) !important;
    }

    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00D4FF, #B537F2, #00FF88) !important;
        border-radius: 999px !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(30, 39, 73, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 212, 255, 0.6) !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3) !important;
        background: rgba(30, 39, 73, 0.95) !important;
    }

    /* Force dark background on expander content */
    .streamlit-expanderContent {
        background: rgba(21, 27, 59, 0.95) !important;
        border: 1px solid rgba(42, 52, 87, 0.8) !important;
        border-radius: 0 0 12px 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Prevent white background on expanded state */
    details[open] > summary {
        background: rgba(30, 39, 73, 0.95) !important;
        border-color: rgba(0, 212, 255, 0.6) !important;
    }

    /* Force all expander content to have dark background */
    details > div {
        background: rgba(21, 27, 59, 0.95) !important;
    }

    details {
        background: transparent !important;
    }

    /* Force all expander text to be visible */
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    .streamlit-expanderContent p,
    .streamlit-expanderContent span,
    .streamlit-expanderContent div {
        color: #FFFFFF !important;
    }

    /* Fix the white overlay issue */
    [data-testid="stExpander"] {
        background: transparent !important;
    }

    [data-testid="stExpander"] > div {
        background: transparent !important;
    }

    /* Override Streamlit's default white background */
    .element-container {
        background: transparent !important;
    }

    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        background: rgba(21, 27, 59, 0.95) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 39, 73, 0.7);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        padding: 12px 24px;
        color: #C8D6FF;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 39, 73, 0.9);
        border-color: rgba(0, 212, 255, 0.6);
        color: #00D4FF;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 212, 255, 0.25) !important;
        border-color: #00D4FF !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Info/Success/Warning Boxes */
    .stAlert {
        background: rgba(30, 39, 73, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
    }

    /* Table Styling */
    .stTable {
        background: rgba(30, 39, 73, 0.5) !important;
        border-radius: 12px !important;
    }

    .stTable thead tr th {
        background: rgba(0, 212, 255, 0.2) !important;
        color: #00D4FF !important;
        font-weight: 600 !important;
        border: none !important;
    }

    .stTable tbody tr td {
        color: #FFFFFF !important;
        border: 1px solid rgba(42, 52, 87, 0.5) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(42, 52, 87, 0.5) !important;
        margin: 32px 0 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }

    h1 {
        color: #FFFFFF !important;
        font-size: 48px !important;
        margin-bottom: 24px !important;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }

    h2, h3 {
        color: #FFFFFF !important;
    }

    /* Make all paragraph text more visible */
    p, span, div {
        color: #E8EEFF !important;
    }

    /* Labels and small text */
    label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* Container Border */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: rgba(30, 39, 73, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
    }

    /* Audio/Video Player */
    audio, video {
        border-radius: 12px !important;
        width: 100% !important;
    }

    /* Custom Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 8px;
    }

    .badge-mp3 {
        background: rgba(0, 212, 255, 0.2);
        color: #00D4FF;
        border: 1px solid rgba(0, 212, 255, 0.4);
    }

    .badge-mp4 {
        background: rgba(181, 55, 242, 0.2);
        color: #B537F2;
        border: 1px solid rgba(181, 55, 242, 0.4);
    }

    .badge-size {
        background: rgba(0, 255, 136, 0.2);
        color: #00FF88;
        border: 1px solid rgba(0, 255, 136, 0.4);
    }

    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(30, 39, 73, 0.5);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00D4FF, #B537F2);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00E5FF, #C547FF);
    }

    /* Override any remaining white backgrounds */
    details {
        background: transparent !important;
    }

    details > div {
        background: transparent !important;
    }

    /* Prevent white flash on state changes */
    * {
        transition: background-color 0s !important;
    }

    button, input, select {
        transition: all 0.3s ease !important;
    }

    /* NUCLEAR OPTION - Force all potential dropdown elements to be dark */
    div[class*="menu"],
    div[class*="Menu"],
    div[class*="option"],
    div[class*="Option"],
    div[class*="list"],
    div[class*="List"],
    ul[class*="menu"],
    ul[class*="Menu"] {
        background: #0F1535 !important;
        color: #E8EEFF !important;
    }

    li[class*="option"],
    li[class*="Option"] {
        background: transparent !important;
        color: #E8EEFF !important;
    }

    li[class*="option"]:hover,
    li[class*="Option"]:hover {
        background: rgba(30, 39, 73, 0.7) !important;
        color: #FFFFFF !important;
    }
</style>

<script>
// Force dropdown styling with JavaScript when dropdown opens
function styleDropdowns() {
    setTimeout(function() {
        // Target all dropdown menus
        const listboxes = document.querySelectorAll('[role="listbox"]');
        listboxes.forEach(function(listbox) {
            listbox.style.setProperty('background', '#0F1535', 'important');
            listbox.style.setProperty('border', '1px solid rgba(0, 212, 255, 0.4)', 'important');
            listbox.style.setProperty('border-radius', '12px', 'important');
            listbox.style.setProperty('padding', '8px', 'important');
        });

        // Target all options
        const options = document.querySelectorAll('[role="option"]');
        options.forEach(function(option) {
            const isSelected = option.getAttribute('aria-selected') === 'true';

            option.style.setProperty('background', isSelected ? 'rgba(0, 212, 255, 0.2)' : 'transparent', 'important');
            option.style.setProperty('color', isSelected ? '#00D4FF' : '#E8EEFF', 'important');
            option.style.setProperty('padding', '14px 18px', 'important');
            option.style.setProperty('margin', '3px 0', 'important');
            option.style.setProperty('border-radius', '10px', 'important');
            option.style.setProperty('font-size', '15px', 'important');
            option.style.setProperty('border', isSelected ? '1px solid rgba(0, 212, 255, 0.5)' : '1px solid transparent', 'important');
        });
    }, 50);
}

// Run when DOM changes (dropdown opens)
const observer = new MutationObserver(styleDropdowns);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)


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


def check_duplicate(title, dl_type):
    folder = SONGS_FOLDER if dl_type == "Music (MP3)" else VIDEOS_FOLDER

    # Normalize title and remove extension for comparison
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


# --- SHARED DOWNLOAD LOGIC (WITH PROGRESS BAR) ---
def perform_download(url, opts, target_folder):
    """
    Executes the download in a separate thread.
    """
    st.info("⏳ Starting download logic...")

    # Create UI Elements for Progress
    progress_bar = st.progress(0)
    status_msg = st.empty()

    # Define Hooks to update the UI
    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%', '')
            try:
                percent_val = float(p) / 100
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')

                # Update UI
                progress_bar.progress(percent_val)
                status_msg.info(f"⚡ Downloading: **{p}%** | Speed: **{speed}** | ETA: **{eta}**")
            except:
                pass
        elif d['status'] == 'finished':
            progress_bar.progress(1.0)
            status_msg.success("✅ Download complete! Finalizing file...")

    # Add hook to opts
    opts['progress_hooks'] = [progress_hook]

    # Run download
    try:
        # FORCE overwrite
        opts['overwrites'] = True
        opts['force_overwrites'] = True

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        st.toast("✅ Download Completed Successfully!", icon="🎉")
        st.session_state.download_done = True
        st.session_state.download_error = None

        # Reset state after successful download
        st.session_state.last_url = ''
        st.session_state.fetched_title = None
        st.session_state.dup = None
        st.session_state.download_done = False
        time.sleep(1)  # Give user a moment to see 100%
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")


# --- CONFIRMATION DIALOG ---
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
                # Close dialog implicitly by finishing
                st.session_state['trigger_download'] = True
                st.rerun()
            except PermissionError:
                st.error("❌ Cannot delete old file. It is currently in use.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    with col2:
        if st.button("❌ No, Cancel", type="secondary", use_container_width=True):
            st.rerun()


# --- HEADER WITH EXIT BUTTON ---
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
    if st.button("🔴 Shutdown App ", key="top_exit", type="secondary"):
        st.success("Stopping server...")
        os._exit(0)

st.markdown("---")

# --- DETAILS EXPANDER ---
with st.expander("📊 Quality & Bitrate Reference Guide"):
    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("#### 🎵 Audio (MP3) Bitrates")
        st.table([
            {"Bitrate": "64 kbps", "Use Case": "Voice/Low Storage"},
            {"Bitrate": "128 kbps", "Use Case": "Standard Mobile"},
            {"Bitrate": "192 kbps", "Use Case": "Good Balance"},
            {"Bitrate": "256 kbps", "Use Case": "High Quality"},
            {"Bitrate": "320 kbps", "Use Case": "Ultra/Best Quality"}
        ])

    with t_col2:
        st.markdown("#### 🎥 Video (MP4) Resolutions")
        st.table([
            {"Res": "144p", "Use Case": "Emergency Saver"},
            {"Res": "360p", "Use Case": "Small Screens"},
            {"Res": "480p", "Use Case": "Standard Definition"},
            {"Res": "720p", "Use Case": "HD Quality"},
            {"Res": "1080p", "Use Case": "Full HD (Sharp)"},
            {"Res": "1440p", "Use Case": "2K / QHD (Highest)"}
        ])

st.markdown("---")

# --- Download Section ---
st.markdown("### 🎯 <span style='color: #FFFFFF; text-shadow: 0 0 10px rgba(0,212,255,0.5);'>Download Media</span>",
            unsafe_allow_html=True)

col_url, col_type, col_qual = st.columns([2, 1, 1])

with col_url:
    url = st.text_input(
        "🔗 YouTube URL",
        placeholder="Paste your YouTube link here...",
        help="Enter a YouTube URL and press Enter to verify",
        label_visibility="collapsed"
    )

with col_type:
    download_type = st.selectbox("📦 Format", ["Music (MP3)", "Video (MP4)"], label_visibility="collapsed")

with col_qual:
    if download_type == "Music (MP3)":
        bitrate = st.selectbox("🎧 Quality", ["64", "128", "192", "256", "320"], index=3, label_visibility="collapsed")
        ydl_format = 'bestaudio/best'
    else:
        quality_choice = st.selectbox("📺 Quality", ["144p", "360p", "480p", "720p", "1080p", "1440p"], index=4,
                                      label_visibility="collapsed")
        height_map = {"144p": 144, "360p": 360, "480p": 480, "720p": 720, "1080p": 1080, "1440p": 1440}
        target_height = height_map[quality_choice]
        ydl_format = f'bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]'

# Force dropdown styling with inline CSS
st.markdown("""
<style>
[data-baseweb="popover"] [data-baseweb="menu"] {
    background-color: #1A2347 !important;
}
[data-baseweb="menu"] ul {
    background-color: #1A2347 !important;
}
[data-baseweb="menu"] li {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session state init ---
if 'last_url' not in st.session_state:
    st.session_state.last_url = ''
if 'fetched_title' not in st.session_state:
    st.session_state.fetched_title = None
if 'dup' not in st.session_state:
    st.session_state.dup = None
if 'download_done' not in st.session_state:
    st.session_state.download_done = False
if 'download_error' not in st.session_state:
    st.session_state.download_error = None
if 'trigger_download' not in st.session_state:
    st.session_state.trigger_download = False

# --- Auto-fetch Metadata Logic ---
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
        try:
            dup_size = format_bytes(os.path.getsize(st.session_state.dup))
        except:
            dup_size = "Unknown"
        # Warning shown, but we continue to show the button
        st.warning(f"⚠️ **File Already Exists!** — `{os.path.basename(st.session_state.dup)}` ({dup_size})")
    else:
        st.info(f"✨ **Ready to Download:** {st.session_state.fetched_title[:80]}...")

# --- PREPARE OPTS (Needed for both button & trigger) ---
ffmpeg_loc = get_ffmpeg_path()
target_folder = SONGS_FOLDER if download_type == "Music (MP3)" else VIDEOS_FOLDER

if download_type == "Music (MP3)":
    opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_loc,
        'outtmpl': f'{SONGS_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate}],
    }
else:
    opts = {
        'format': ydl_format,
        'ffmpeg_location': ffmpeg_loc,
        'outtmpl': f'{VIDEOS_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
    }

# --- HANDLE TRIGGERED DOWNLOAD (From Dialog) ---
if st.session_state.get('trigger_download'):
    st.session_state.trigger_download = False  # Reset flag
    perform_download(url, opts, target_folder)

# --- DOWNLOAD BUTTON ---
if st.button("🚀 Start Download", use_container_width=True):
    if not url:
        st.warning("⚠️ Please enter a URL!")
    else:
        # Check Duplicate Logic
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

# --- Library Section ---
st.markdown("---")
st.markdown("### 📚 <span style='color: #FFFFFF; text-shadow: 0 0 10px rgba(0,212,255,0.5);'>Your Library</span>",
            unsafe_allow_html=True)
tab_music, tab_video = st.tabs(["🎵 Music Collection", "🎥 Video Collection"])

# --- MUSIC TAB ---
with tab_music:
    files = [f for f in os.listdir(SONGS_FOLDER) if f.endswith('.mp3')]
    if files:
        for f in files:
            file_path = os.path.join(SONGS_FOLDER, f)
            try:
                file_size = os.path.getsize(file_path)
                size_str = format_bytes(file_size)
            except:
                size_str = "Unknown"

            with st.expander(f"🎶 **{f}**"):
                st.markdown(f'<span class="badge badge-mp3">MP3</span><span class="badge badge-size">{size_str}</span>',
                            unsafe_allow_html=True)
                st.audio(file_path)
                if st.button(f"🗑️ Delete", key=f"del_{f}"):
                    os.remove(file_path)
                    st.rerun()
    else:
        st.info("🎵 Your music library is empty. Start downloading!")

# --- VIDEO TAB ---
with tab_video:
    v_files = [f for f in os.listdir(VIDEOS_FOLDER) if f.endswith('.mp4')]
    if v_files:
        for f in v_files:
            file_path = os.path.join(VIDEOS_FOLDER, f)
            try:
                file_size = os.path.getsize(file_path)
                size_str = format_bytes(file_size)
            except:
                size_str = "Unknown"

            with st.expander(f"🎬 **{f}**"):
                st.markdown(f'<span class="badge badge-mp4">MP4</span><span class="badge badge-size">{size_str}</span>',
                            unsafe_allow_html=True)
                st.video(file_path)
                if st.button(f"🗑️ Delete", key=f"del_v_{f}"):
                    os.remove(file_path)
                    st.rerun()
    else:
        st.info("🎥 Your video library is empty. Start downloading!")

# --- Storage Indicator ---
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

# --- FOOTER ---
st.markdown("---")

footer_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: transparent; font-family: 'Poppins', sans-serif; overflow: hidden; }

    .footer {
        position: relative;
        text-align: center;
        padding: 28px 20px;
        border-radius: 20px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        background: rgba(10, 15, 40, 0.85);
        backdrop-filter: blur(20px);
        overflow: hidden;
    }

    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        pointer-events: none;
        animation: float 6s ease-in-out infinite;
    }
    .orb1 { width:200px; height:200px; background:rgba(0,212,255,0.15); top:-80px; left:-60px; animation-delay:0s; }
    .orb2 { width:180px; height:180px; background:rgba(181,55,242,0.15); top:-60px; right:-50px; animation-delay:2s; }
    .orb3 { width:150px; height:150px; background:rgba(0,255,136,0.1); bottom:-60px; left:40%; animation-delay:4s; }

    @keyframes float {
        0%,100% { transform: translateY(0px) scale(1); }
        50%       { transform: translateY(-15px) scale(1.05); }
    }

    .glow-line {
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #00D4FF, #B537F2, #00FF88, #00D4FF, transparent);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }

    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position:  200% 0; }
    }

    .tech-badges {
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 16px;
    }

    .badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        animation: badgepulse 2s ease-in-out infinite;
    }

    .badge-py { background:rgba(55,120,200,0.2); color:#5ba3f5; border:1px solid rgba(55,120,200,0.4); animation-delay:0s; }
    .badge-st { background:rgba(255,75,75,0.2);  color:#ff6b6b; border:1px solid rgba(255,75,75,0.4);  animation-delay:0.3s; }
    .badge-yt { background:rgba(255,0,0,0.15);   color:#ff4444; border:1px solid rgba(255,0,0,0.3);    animation-delay:0.6s; }
    .badge-ff { background:rgba(0,212,255,0.15); color:#00D4FF; border:1px solid rgba(0,212,255,0.3);  animation-delay:0.9s; }
    .badge-ig { background:rgba(181,55,242,0.2); color:#B537F2; border:1px solid rgba(181,55,242,0.4); animation-delay:1.2s; }

    @keyframes badgepulse {
        0%,100% { transform:translateY(0); box-shadow:none; }
        50%       { transform:translateY(-2px); box-shadow:0 4px 15px rgba(0,212,255,0.3); }
    }

    .footer-title {
        font-size: 15px;
        font-weight: 700;
        background: linear-gradient(135deg, #00D4FF, #B537F2, #00FF88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }

    .legal {
        font-size: 11px;
        color: #5a6a8a;
        line-height: 1.7;
        margin-bottom: 14px;
        padding: 10px 16px;
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .legal strong { color: #8899bb; }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
        margin: 12px 0;
    }

    .copyright { font-size: 11px; color: #3a4a6a; letter-spacing: 0.3px; }
    .copyright span { color: #00D4FF; font-weight: 600; }

    .heart {
        display: inline-block;
        animation: heartbeat 1.2s ease-in-out infinite;
        color: #ff4466 !important;
        -webkit-text-fill-color: #ff4466 !important;
        font-size: 16px;
        filter: drop-shadow(0 0 6px rgba(255, 68, 102, 0.8));
    }
    @keyframes heartbeat {
        0%,100% { transform:scale(1); }
        14%       { transform:scale(1.3); }
        28%       { transform:scale(1); }
        42%       { transform:scale(1.3); }
        70%       { transform:scale(1); }
    }
</style>
</head>
<body>
<div class="footer">
    <div class="glow-line"></div>
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>

    <div class="tech-badges">
        <span class="badge badge-py">🐍 Python</span>
        <span class="badge badge-st">⚡ Streamlit</span>
        <span class="badge badge-yt">📥 yt-dlp</span>
        <span class="badge badge-ff">🎬 FFmpeg</span>
    </div>

    <div class="footer-title">
        Built with <span class="heart">❤️</span> by Krishna Malgi
    </div>

    <div class="legal">
        ⚖️ <strong>Legal Disclaimer:</strong> This tool is intended for personal use only.
        Users are responsible for compliance with copyright laws & platform Terms of Service.
        Downloading copyrighted content without authorization may be unlawful in your jurisdiction.
    </div>

    <div class="divider"></div>

    <div class="copyright">
        © 2026 <span>Pro Media Downloader</span> • All rights reserved • Developed by <span>Krishna Malgi</span>
    </div>
</div>
</body>
</html>
"""

components.html(footer_html, height=300)