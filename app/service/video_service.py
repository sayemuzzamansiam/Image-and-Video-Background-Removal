# app/service/video_service.py

import tempfile
import os
import cv2
from rembg import remove

def write_temp_file(file_bytes, suffix=""):
    """Write bytes to a temporary file and return its path"""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as tmp:
        tmp.write(file_bytes)
    return path

def remove_bg_video_bytes(video_bytes):
    in_path = write_temp_file(video_bytes, suffix=".mp4")
    out_path = in_path.replace(".mp4", "_out.mp4")

    cap = cv2.VideoCapture(in_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height), True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no_bg = remove(frame)

        if frame_no_bg.shape[2] == 4:
            frame_no_bg = cv2.cvtColor(frame_no_bg, cv2.COLOR_BGRA2BGR)

        out.write(frame_no_bg)

    cap.release()
    out.release()

    with open(out_path, "rb") as f:
        result_bytes = f.read()

    os.remove(in_path)
    os.remove(out_path)

    return result_bytes
