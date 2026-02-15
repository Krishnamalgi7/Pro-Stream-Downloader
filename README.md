# 🚀 Pro Media Downloader (YouTube Edition)

A high-performance YouTube to MP3/MP4 converter designed for high-fidelity media archiving.

---

## 📸 Overview

This application leverages the power of **yt-dlp** to bypass YouTube's standard limitations, allowing you to extract audio and video at the highest possible quality directly to your local machine.

---

## ✨ Specialized YouTube Features

### 🎯 Pure Audio Extraction
Specifically extracts the best audio streams (Opus/m4a) and converts them to high-bitrate **320kbps MP3**.

### 📺 High-Resolution Video
Handles YouTube's DASH streams to merge separate video and audio tracks into a single, high-quality **1080p** or **1440p (2K) MP4**.

### 🧠 Smart Content Awareness
Detects video titles and thumbnails instantly.

### 🔄 Quality Upgrade Logic
If you previously downloaded a video in 360p, the app detects it and offers to **Replace** it with a 1080p version to keep your library optimized.

### 📊 YouTube Progress Sync
Real-time feedback using YouTube-specific metadata for speed tracking and ETA.

---

## 🛠️ Installation & Setup

### 1. Requirements

- **Python 3.10+**
- **FFmpeg**: Essential for YouTube video/audio merging (Included in this repo)
- **Node.js**: Recommended to help yt-dlp process YouTube's JavaScript signatures faster

### 2. Local Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Songs_downloader.git
   cd Songs_downloader
   ```

2. **Install core dependencies:**
   ```bash
   pip install streamlit yt-dlp
   ```

3. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Folder Architecture

```
Songs_downloader/
├── data/
│   ├── songs/          # Organized YouTube MP3s
│   └── videos/         # Organized YouTube MP4s
├── app.py              # Main Application Logic
├── ffmpeg.exe          # The "Engine" for YouTube merging
└── README.md           # Documentation
```

---

## ⚖️ YouTube Quality Guide

| Format | Selection      | Use Case                              |
|--------|----------------|---------------------------------------|
| MP3    | 320 kbps       | Audiophile archiving                  |
| MP3    | 128 kbps       | Fast mobile storage                   |
| MP4    | 1080p          | High Definition TVs/Monitors          |
| MP4    | 720p           | Standard HD Viewing                   |
| MP4    | 1440p (2K)     | Ultra-sharp professional displays     |

---

## 📜 License & Legal

This project is licensed under the **MIT License**.

**⚠️ Disclaimer:** This tool is intended for personal use and archiving educational content. Please respect YouTube's Terms of Service and only download content for which you have the legal right or permission.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YOUR_USERNAME/Songs_downloader/issues).

---

## 👤 Author

**Your Name**
- GitHub: [@krishnamalgi7](https://github.com/krishnamalgi7)

---

**⭐ Star this repo if you find it useful! ⭐**
