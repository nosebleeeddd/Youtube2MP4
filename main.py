from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import re


def safe_filename(name):
    # Remove characters that can cause filename/path problems
    return re.sub(r'[\\/*?:"<>|]', "", name)


def download_video(url, save_path):
    try:
        print("Loading YouTube video...")

        yt = YouTube(url)

        print(f"Title: {yt.title}")

        # Best video-only MP4 stream
        video_stream = (
            yt.streams
            .filter(
                adaptive=True,
                only_video=True,
                file_extension="mp4"
            )
            .order_by("resolution")
            .desc()
            .first()
        )

        # Best audio-only MP4/M4A-compatible stream
        audio_stream = (
            yt.streams
            .filter(
                adaptive=True,
                only_audio=True,
                file_extension="mp4"
            )
            .order_by("abr")
            .desc()
            .first()
        )

        if video_stream is None:
            print("No compatible video stream found.")
            return

        if audio_stream is None:
            print("No compatible audio stream found.")
            return

        print(
            f"Video stream: {video_stream.resolution} "
            f"{video_stream.mime_type}"
        )

        print(
            f"Audio stream: {audio_stream.abr} "
            f"{audio_stream.mime_type}"
        )

        # Temporary filenames
        temp_video = os.path.join(save_path, "temp_video.mp4")
        temp_audio = os.path.join(save_path, "temp_audio.m4a")

        title = safe_filename(yt.title)

        output_file = os.path.join(
            save_path,
            f"{title}.mp4"
        )

        print("\nDownloading video...")
        video_stream.download(
            output_path=save_path,
            filename="temp_video.mp4"
        )

        print("Downloading audio...")
        audio_stream.download(
            output_path=save_path,
            filename="temp_audio.m4a"
        )

        print("\nMerging video and audio with FFmpeg...")

        subprocess.run(
            [
                "ffmpeg",
                "-y",

                # video
                "-i",
                temp_video,

                # audio
                "-i",
                temp_audio,

                # don't re-encode the video
                "-c:v",
                "copy",

                # copy the AAC audio
                "-c:a",
                "copy",

                # stop when shortest stream ends
                "-shortest",

                # Better MP4 playback/streaming compatibility
                "-movflags",
                "+faststart",

                output_file
            ],
            check=True
        )

        # Delete temporary files
        if os.path.exists(temp_video):
            os.remove(temp_video)

        if os.path.exists(temp_audio):
            os.remove(temp_audio)

        print("\nDownload complete!")
        print(f"Saved to: {output_file}")

    except subprocess.CalledProcessError:
        print("FFmpeg failed while merging the files.")

    except Exception as e:
        print(f"Download failed: {e}")


def open_folder_dialog():
    folder = filedialog.askdirectory()

    if folder:
        print(f"Selected folder: {folder}")

    return folder


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    video_url = input(
        "Please enter a YouTube URL: "
    ).strip()

    save_dir = open_folder_dialog()

    if save_dir:
        print("\nStarting download...\n")
        download_video(video_url, save_dir)
    else:
        print("Invalid save location.")
