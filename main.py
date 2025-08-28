import os
import uuid
import yt_dlp
import streamlit as st
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import uvicorn
import threading

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        final_path = ydl.prepare_filename(info)  # actual downloaded file
    return final_path

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
                    st.download_button(
                        label="Download File",
                        data=open(file_path, "rb").read(),
                        file_name=os.path.basename(file_path),
                    )
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a URL.")

# ==============================
# FASTAPI BACKEND
# ==============================
app = FastAPI()

@app.get("/download")
def download_api(url: str = Query(..., description="Media URL to download")):
    try:
        file_path = download_media(url)
        return FileResponse(file_path, filename=os.path.basename(file_path))
    except Exception as e:
        return {"error": str(e)}

# ==============================
# RUN BOTH STREAMLIT + FASTAPI
# ==============================
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Run FastAPI in background thread
    threading.Thread(target=run_fastapi, daemon=True).start()
    # Run Streamlit
    streamlit_app()
