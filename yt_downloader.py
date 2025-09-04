import os
import threading
import yt_dlp
import customtkinter as ctk
from tkinter import filedialog, messagebox

# -- Download Function -- #
def download_video():
    url = url_entry.get()
    choice = format_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    folder = filedialog.askdirectory(title="Select Download Folder")
    if not folder:
        return

    try:
        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'quiet': True,
            'ffmpeg_location': r"C:\Users\admin\Downloads\SetUp\ffmpeg-2025-09-01-git-3ea6c2fe25-full_build\bin",  # <-- Palitan ng Path kung saan nakalagay ang bin
            'extractor_args': {
                'youtube': {'player-client': ['web']}
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/120.0.0.0 Safari/537.36'
            }
        }

        # Format selection
        if choice == "mp4":
            ydl_opts['format'] = 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/mp4'
            ydl_opts['merge_output_format'] = 'mp4'
        elif choice == "mp3":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            status_label.configure(text="Please select MP3 or MP4!", text_color="red")
            return

        status_label.configure(text="Downloading...", text_color="yellow")
        window.update_idletasks()

        # Start downloading
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.configure(text="Download Complete!", text_color="green")
        messagebox.showinfo("Success", "Download finished successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed: {str(e)}")
        status_label.configure(text="Download Failed!", text_color="red")

def start_download():
    thread = threading.Thread(target=download_video)
    thread.start()

# -- UI DESIGN -- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.title("YouTube MP3 & MP4 Downloader")
window.geometry("550x350")
window.resizable(False, False)

# Title
title_label = ctk.CTkLabel(window, text="YouTube Downloader", font=ctk.CTkFont(size=22, weight="bold"))
title_label.pack(pady=15)

# URL Entry
url_entry = ctk.CTkEntry(window, width=400, height=35, placeholder_text="Paste YouTube link here")
url_entry.pack(pady=10)

# Format Selection
format_var = ctk.StringVar(value="mp4")
format_frame = ctk.CTkFrame(window)
format_frame.pack(pady=10)

mp4_radio = ctk.CTkRadioButton(format_frame, text="MP4 (Video)", variable=format_var, value="mp4")
mp3_radio = ctk.CTkRadioButton(format_frame, text="MP3 (Audio)", variable=format_var, value="mp3")
mp4_radio.grid(row=0, column=0, padx=15)
mp3_radio.grid(row=0, column=1, padx=15)

# Download Button
download_btn = ctk.CTkButton(window, text="Download", width=200, height=40, command=start_download)
download_btn.pack(pady=20)

# Status Label
status_label = ctk.CTkLabel(window, text="", font=ctk.CTkFont(size=13))
status_label.pack(pady=5)

# Footer
footer_label = ctk.CTkLabel(window, text="Created by Alecs", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray")
footer_label.pack(side="bottom", pady=10)

# Run App
window.mainloop()

