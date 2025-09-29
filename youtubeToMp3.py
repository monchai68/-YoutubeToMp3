#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube to MP3 Converter
A simple GUI application to download YouTube videos and convert them to MP3 format.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import re
from urllib.parse import urlparse, parse_qs
import yt_dlp
import tempfile


class YouTubeToMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to MP3 Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Create download folder if it doesn't exist
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_MP3")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube to MP3 Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Paste button
        paste_btn = ttk.Button(main_frame, text="Paste", command=self.paste_url)
        paste_btn.grid(row=1, column=2, padx=(10, 0), pady=5)
        
        # Output folder selection
        ttk.Label(main_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.folder_var = tk.StringVar(value=self.download_folder)
        self.folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=50)
        self.folder_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Browse button
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=2, column=2, padx=(10, 0), pady=5)
        
        # Format selection (MP3/MP4) with Radio Buttons
        ttk.Label(main_frame, text="Output Format:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="mp3")
        
        # Create frame for radio buttons
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # MP3 Radio Button
        mp3_radio = ttk.Radiobutton(format_frame, text="MP3 (Audio)", 
                                   variable=self.format_var, value="mp3",
                                   command=self.on_format_change)
        mp3_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        # MP4 Radio Button
        mp4_radio = ttk.Radiobutton(format_frame, text="MP4 (Video)", 
                                   variable=self.format_var, value="mp4",
                                   command=self.on_format_change)
        mp4_radio.pack(side=tk.LEFT)
        
        # Quality selection
        ttk.Label(main_frame, text="Quality:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="best")
        self.quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                        values=["best", "320", "256", "192", "128"], 
                                        state="readonly", width=10)
        self.quality_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download & Convert to MP3", 
                                     command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Progress info frame
        progress_info_frame = ttk.Frame(main_frame)
        progress_info_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        progress_info_frame.columnconfigure(0, weight=1)
        progress_info_frame.columnconfigure(1, weight=1)
        progress_info_frame.columnconfigure(2, weight=1)
        
        # Progress percentage
        self.progress_percent_var = tk.StringVar(value="0%")
        progress_percent_label = ttk.Label(progress_info_frame, textvariable=self.progress_percent_var, 
                                         font=('Arial', 9, 'bold'))
        progress_percent_label.grid(row=0, column=0, sticky=tk.W)
        
        # Download speed
        self.speed_var = tk.StringVar(value="Speed: ---")
        speed_label = ttk.Label(progress_info_frame, textvariable=self.speed_var)
        speed_label.grid(row=0, column=1, sticky=tk.W)
        
        # Time remaining
        self.eta_var = tk.StringVar(value="ETA: ---")
        eta_label = ttk.Label(progress_info_frame, textvariable=self.eta_var)
        eta_label.grid(row=0, column=2, sticky=tk.W)
        
        # File size info
        progress_size_frame = ttk.Frame(main_frame)
        progress_size_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        progress_size_frame.columnconfigure(0, weight=1)
        progress_size_frame.columnconfigure(1, weight=1)
        
        # Downloaded size
        self.downloaded_var = tk.StringVar(value="Downloaded: ---")
        downloaded_label = ttk.Label(progress_size_frame, textvariable=self.downloaded_var, 
                                   font=('Arial', 8))
        downloaded_label.grid(row=0, column=0, sticky=tk.W)
        
        # Total size
        self.total_size_var = tk.StringVar(value="Total: ---")
        total_size_label = ttk.Label(progress_size_frame, textvariable=self.total_size_var,
                                   font=('Arial', 8))
        total_size_label.grid(row=0, column=1, sticky=tk.W)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               font=('Arial', 10, 'bold'))
        status_label.grid(row=9, column=0, columnspan=3, pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Download Log", padding="5")
        log_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(10, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for log text
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Clear log button
        clear_btn = ttk.Button(main_frame, text="Clear Log & URL", command=self.clear_log)
        clear_btn.grid(row=11, column=0, pady=5, sticky=tk.W)
        
        # Open folder button
        open_folder_btn = ttk.Button(main_frame, text="Open Download Folder", 
                                   command=self.open_download_folder)
        open_folder_btn.grid(row=11, column=2, pady=5, sticky=tk.E)
        
    def paste_url(self):
        """Paste URL from clipboard"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.url_var.set(clipboard_text)
        except tk.TclError:
            self.log("No text in clipboard")
            
    def browse_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)
            self.download_folder = folder
            
    def clear_log(self):
        """Clear the log text area and URL input"""
        self.log_text.delete(1.0, tk.END)
        self.url_var.set("")  # Clear URL input
        self.log("Log and URL cleared")
        
    def open_download_folder(self):
        """Open the download folder in file explorer"""
        if os.path.exists(self.download_folder):
            os.startfile(self.download_folder)
        else:
            self.log("Download folder does not exist")
            
    def on_format_change(self):
        """Handle format change event"""
        format_choice = self.format_var.get()
        if format_choice == "mp3":
            # For MP3, show audio quality options
            self.quality_combo['values'] = ["best", "320", "256", "192", "128"]
            self.download_btn.configure(text="Download & Convert to MP3")
            self.log("Format changed to MP3 (Audio only)")
        else:  # mp4
            # For MP4, show video quality options
            self.quality_combo['values'] = ["best", "1080p", "720p", "480p", "360p"]
            self.download_btn.configure(text="Download as MP4")
            self.log("Format changed to MP4 (Video with Audio)")
        
        self.quality_var.set("best")  # Reset to best quality
            
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_status(self, message):
        """Update status label"""
        self.status_var.set(message)
        self.root.update()
        
    def update_progress(self, percentage):
        """Update progress bar"""
        self.progress_var.set(percentage)
        self.progress_percent_var.set(f"{percentage:.1f}%")
        self.root.update()
        
    def reset_progress_info(self):
        """Reset all progress information"""
        self.progress_var.set(0)
        self.progress_percent_var.set("0%")
        self.speed_var.set("Speed: ---")
        self.eta_var.set("ETA: ---")
        self.downloaded_var.set("Downloaded: ---")
        self.total_size_var.set("Total: ---")
        self.root.update()
        
    def validate_youtube_url(self, url):
        """Validate if the URL is a valid YouTube URL"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
        
    def progress_hook(self, d):
        """Progress hook for yt-dlp with detailed information"""
        if d['status'] == 'downloading':
            try:
                # Get percentage
                percent_str = d.get('_percent_str', '0%').replace('%', '')
                try:
                    percent = float(percent_str)
                except:
                    percent = 0
                
                # Update progress bar
                self.update_progress(percent)
                
                # Get speed
                speed = d.get('_speed_str', 'N/A')
                if speed != 'N/A':
                    self.speed_var.set(f"Speed: {speed}")
                
                # Get ETA (time remaining)
                eta = d.get('_eta_str', 'N/A')
                if eta != 'N/A' and eta != 'Unknown':
                    self.eta_var.set(f"ETA: {eta}")
                
                # Get downloaded and total size
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                
                if downloaded_bytes > 0:
                    downloaded_mb = downloaded_bytes / (1024 * 1024)
                    self.downloaded_var.set(f"Downloaded: {downloaded_mb:.1f} MB")
                
                if total_bytes > 0:
                    total_mb = total_bytes / (1024 * 1024)
                    self.total_size_var.set(f"Total: {total_mb:.1f} MB")
                
                # Update status with detailed info
                status_msg = f"Downloading... {percent:.1f}%"
                if speed != 'N/A':
                    status_msg += f" | {speed}"
                if eta != 'N/A' and eta != 'Unknown':
                    status_msg += f" | ETA: {eta}"
                    
                self.update_status(status_msg)
                
            except Exception as e:
                # Fallback to basic progress
                try:
                    percent = float(d.get('_percent_str', '0').replace('%', ''))
                    self.update_progress(percent)
                    self.update_status(f"Downloading... {percent:.1f}%")
                except:
                    self.update_status("Downloading...")
                    
        elif d['status'] == 'finished':
            self.update_progress(100)
            self.update_status("Download completed, processing...")
            self.log(f"✓ Downloaded: {d.get('filename', 'file')}")
            
        elif d['status'] == 'error':
            self.update_status("Download error occurred")
            self.log(f"❌ Download error: {d.get('error', 'Unknown error')}")
            
    def download_youtube_video(self, url, output_path, quality, format_choice):
        """Download YouTube video as MP3 or MP4"""
        try:
            # Reset progress information
            self.reset_progress_info()
            
            # Configure yt-dlp options based on format choice
            if format_choice == "mp3":
                # Set audio quality for MP3
                audio_quality = quality if quality != 'best' else '320'
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                    'progress_hooks': [self.progress_hook],
                    'noplaylist': True,
                    'writeinfojson': False,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                }
            else:  # mp4
                if quality == "best":
                    format_selector = 'best[ext=mp4]'
                elif quality == "1080p":
                    format_selector = 'best[height<=1080][ext=mp4]'
                elif quality == "720p":
                    format_selector = 'best[height<=720][ext=mp4]'
                elif quality == "480p":
                    format_selector = 'best[height<=480][ext=mp4]'
                elif quality == "360p":
                    format_selector = 'best[height<=360][ext=mp4]'
                else:
                    format_selector = 'best[ext=mp4]'
                    
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'noplaylist': True,
                }
                
            self.log(f"Starting download from: {url}")
            self.log(f"Format: {format_choice.upper()}, Quality: {quality}")
            self.update_status("Initializing download...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                filesize = info.get('filesize') or info.get('filesize_approx')
                
                self.log(f"Title: {title}")
                self.log(f"Duration: {duration//60}:{duration%60:02d}")
                
                if filesize:
                    filesize_mb = filesize / (1024 * 1024)
                    self.log(f"Estimated size: {filesize_mb:.1f} MB")
                    self.total_size_var.set(f"Total: {filesize_mb:.1f} MB")
                
                # Download and convert
                self.log("Downloading and processing...")
                ydl.download([url])
                
            # Final progress update
            self.update_progress(100)
            self.progress_percent_var.set("100% - Complete!")
            self.speed_var.set("Speed: Complete")
            self.eta_var.set("ETA: Done")
            
            if format_choice == "mp3":
                self.update_status("MP3 conversion completed successfully!")
                self.log("✓ Download and MP3 conversion completed successfully!")
                messagebox.showinfo("Success", f"Successfully downloaded and converted to MP3:\n{title}")
            else:
                self.update_status("MP4 download completed successfully!")
                self.log("✓ MP4 download completed successfully!")
                messagebox.showinfo("Success", f"Successfully downloaded MP4:\n{title}")
            
        except Exception as e:
            error_msg = f"Error during download: {str(e)}"
            self.log(f"❌ {error_msg}")
            self.update_status("Download failed")
            messagebox.showerror("Error", error_msg)
        finally:
            self.download_btn.configure(state="normal")
            # Keep progress info visible for a few seconds before reset
            self.root.after(3000, self.reset_progress_info)
            
    def start_download(self):
        """Start the download process in a separate thread"""
        url = self.url_var.get().strip()
        output_path = self.folder_var.get().strip()
        quality = self.quality_var.get()
        format_choice = self.format_var.get()
        
        # Validation
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        if not self.validate_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
            
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output folder: {e}")
                return
        
        # Disable download button during processing
        self.download_btn.configure(state="disabled")
        
        # Start download in separate thread
        download_thread = threading.Thread(
            target=self.download_youtube_video, 
            args=(url, output_path, quality, format_choice)
        )
        download_thread.daemon = True
        download_thread.start()


def main():
    """Main function"""
    root = tk.Tk()
    app = YouTubeToMP3Converter(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
