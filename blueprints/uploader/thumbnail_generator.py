import os, sys
from moviepy.editor import VideoFileClip
from PIL import Image

def generate_thumbnail(video_file, output_dir) -> None:
    try:
        if os.path.exists:
            file_output_name = video_file[16:-4]
            clip = VideoFileClip(video_file)
            frame = int((clip.duration)+1) // 2
            thumbnail = clip.get_frame(frame)
            new_image_file = os.path.join(output_dir, f'{file_output_name}.jpg')
            new_image = Image.fromarray(thumbnail)
            new_image.save(new_image_file)
    except OSError:
        print('Could not load file from given path!')
        raise
