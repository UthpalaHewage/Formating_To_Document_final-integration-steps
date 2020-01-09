"""Intermediate module to connect GUI and main 3 component"""
import frame_seperator

# create the object of the frame_seperator module
FRAME_SEPARATOR_OBJ = frame_seperator.FrameSeperator()


def start_generation(video_location, transcript_location, save_location):
    """run after button click and manage input and outputs for each module"""
    # command to start the visual content analysis
    FRAME_SEPARATOR_OBJ.catch_video(video_location)
