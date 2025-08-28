import os
import uuid
import yt_dlp
import streamlit as st

# ==============================
# CONFIG
# ==============================
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ==============================
# DOWNLOAD FUNCTION
# ==============================
def download_media(url: str) -> str:
    """Download from TikTok, YouTube, Instagram, etc. using yt-dlp"""
    file_id = str(uuid.uuid4())  # unique filename
    file_path = os.path.join(DOWNLOAD_DIR, file_id + ".%(ext)s")

    ydl_opts = {
        "outtmpl": file_path,
        "format": "best",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            final_path = ydl.prepare_filename(info)  # actual downloaded file
        return final_path
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

# ==============================
# STREAMLIT UI
# ==============================
def streamlit_app():
    st.title("📥 Universal Media Downloader")
    st.write("Download from TikTok, YouTube, Instagram, etc. using yt-dlp")

    url = st.text_input("Enter URL here:")

    if st.button("Download"):
        if url:
            with st.spinner("Downloading..."):
                try:
                    file_path = download_media(url)
                    st.success("✅ Download complete!")
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="Download File",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime="application/octet-stream",
                        )
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    streamlit_app()