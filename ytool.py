#!/usr/bin/env python3
import sys
import subprocess
import os
import platform

def print_help():
    print("用法: ytool <opt> <file> <dest>")
    print("選項:")
    print("  -a, --audio    下載最佳音訊 (優先 webm)")
    print("  -v, --video    下載最佳影片 (含音訊)")
    print("  -h, --help     顯示本幫助訊息")
    print("參數:")
    print("  <file>   包含網址清單的檔案")
    print("  <dest>   下載檔案的目的資料夾")

def get_ffmpeg_location():
    system = platform.system().lower()
    if system == "windows":
        ffmpeg_exe = os.path.join(os.getcwd(), "ffmpeg.exe")
        return ffmpeg_exe if os.path.exists(ffmpeg_exe) else None
    else:
        return None  # use system ffmpeg

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        return

    opt = sys.argv[1]
    if len(sys.argv) < 3:
        print("錯誤: 缺少 <file> 參數")
        print_help()
        return

    file_path = sys.argv[2]
    if not os.path.exists(file_path):
        print(f"錯誤: 找不到檔案 {file_path}")
        return

    if len(sys.argv) < 4:
        print("錯誤: 缺少 <dest> 參數")
        print_help()
        return

    dest_dir = sys.argv[3]
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    ffmpeg_loc = get_ffmpeg_location()

    # 根據選項決定 yt-dlp 參數
    if opt in ("-a", "--audio"):
        command_template = [
            "yt-dlp",
            "-f", "bestaudio[ext=webm]/bestaudio",
            "-o", os.path.join(dest_dir, "%(title)s.%(ext)s")
        ]
    elif opt in ("-v", "--video"):
        command_template = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",
            "-o", os.path.join(dest_dir, "%(title)s.%(ext)s")
        ]
        if ffmpeg_loc:
            command_template.insert(1, "--ffmpeg-location")
            command_template.insert(2, ffmpeg_loc)
    else:
        print("錯誤: 未知選項")
        print_help()
        return

    # 逐行讀取網址
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if url:
                print(f"正在下載: {url}")
                try:
                    subprocess.run(command_template + [url], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"下載失敗: {url} (錯誤碼 {e.returncode})")

if __name__ == "__main__":
    main()
