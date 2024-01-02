import cv2, os
from BasicParams import *


def convertToGray(name, input_file=INPUT_FILE, output_path=OUTPUT_PATH):
    """
    Purpose: This function will convert a video into Grayscale format.
    param: name: The target file's name.
    param input_file: Literal meaning.
    param output_path: The target path of the file.
    return: None
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    vid = cv2.VideoCapture(input_file)  # Get the original video
    file = f"{output_path}{name}.avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    vid_writer = cv2.VideoWriter(file, fourcc, FPS, RESOLUTION, isColor=False)
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    for frame_count in range(total_frames):
        _, frame = vid.read()
        if frame is None:
            print(f"Fail to get this pic at {frame_count}.")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vid_writer.write(frame)
    vid.release()
    vid_writer.release()
