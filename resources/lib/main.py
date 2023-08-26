import xbmcgui
import xbmcaddon
import subprocess
import os
import sys

# Pobranie ustawień z pliku ustawień wtyczki
addon = xbmcaddon.Addon(id='plugin.program.cuts')
recordings_directory = addon.getSetting('recordings_directory')
output_directory = addon.getSetting('output_directory')
ffmpeg_executable = addon.getSetting('ffmpeg_executable')

# Funkcja wyświetlająca okno przeglądania katalogów i wybierania pliku wideo
def browse_for_video():
    dialog = xbmcgui.Dialog()
    video_path = dialog.browseSingle(1, 'Wybierz plik wideo', 'video', '.mp4|.avi|.mkv', False, False, recordings_directory)
    return video_path

# Funkcja obsługująca wycinanie wideo
def trim_video(input_path, start_time, end_time, output_path):
    filename = os.path.basename(input_path)  # Pobranie nazwy pliku
    start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    end_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(end_time.split(":"))))
    duration_seconds = end_time_seconds - start_time_seconds
    trimmed_filename = f"trimmed_{filename[:-4]}_{start_time.replace(':', '')}_{duration_seconds}s.mp4"
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,
        "-ss", start_time,
        "-to", end_time,
        "-c:v", "copy",
        "-c:a", "copy",
        os.path.join(output_directory, trimmed_filename)
    ]
    subprocess.run(ffmpeg_cmd)

# Pobranie wybranego pliku wideo
selected_video = browse_for_video()

if selected_video:
    dialog = xbmcgui.Dialog()
    start_time = dialog.input("Podaj początkowy czas (np. 00:00:00):")
    end_time = dialog.input("Podaj końcowy czas (np. 00:02:30):")

    if start_time and end_time:
        output_path = os.path.join(output_directory, "trimmed_video.mp4")
        trim_video(selected_video, start_time, end_time, output_path)
        xbmcgui.Dialog().notification("Sukces", "Wycinek zapisano jako trimmed_video-Sygnatura.mp4", xbmcgui.NOTIFICATION_INFO)
