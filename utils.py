import ffmpeg
import os


def convert_to_mp4(input_path: str, output_path: str):
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path)
    ffmpeg.run(stream)


def get_file_size(file_path: str) -> float:
    return os.path.getsize(file_path) / (1024 * 1024)
