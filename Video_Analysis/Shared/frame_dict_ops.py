"""Manage the frame info using unique frame detail info object"""

import Models.unique_frame_detail_dict as dict_frame_detail
import Models.unique_frame_detail as obj


class DictOps(object):
    """class for manage frame info to get relevantly"""

    # constructor
    def __init__(self):
        pass

    # method - add figure to dict
    # figure are fill first so other elements are None and False
    # here key is frame position
    @classmethod
    def add_to_dict_from_figure(cls, frame_position, time_stamp):
        dict_frame_detail.frame_dict.update(
            {frame_position: obj.FrameDetail(frame_position, False, None, False, None, True, time_stamp)})

    # method
    # add texts->content and subtitle to dict
    # here key is frame position
    @classmethod
    def add_to_dict_from_text_extract(cls, frame_position, title_availability, title, content_availability, content,
                                      time_stamp):
        # frame position is already contain means this frame contain a figure
        if dict_frame_detail.frame_dict.__contains__(frame_position):
            dict_frame_detail.frame_dict.update(
                {frame_position: obj.FrameDetail(frame_position, title_availability, title,
                                                 content_availability, content, True, time_stamp)})
        # not contain a figure
        else:
            dict_frame_detail.frame_dict.update(
                {frame_position: obj.FrameDetail(frame_position, title_availability, title,
                                                 content_availability, content, False, time_stamp)})

    # method - print the result
    @classmethod
    def view_dict(cls):

        for key in dict_frame_detail.frame_dict:
            print(dict_frame_detail.frame_dict[key].frame_position)
            print(" ")
            print(dict_frame_detail.frame_dict[key].title_availability)
            print(" ")
            print(dict_frame_detail.frame_dict[key].title)
            print(" ")
            print(dict_frame_detail.frame_dict[key].content_availability)
            print(" ")
            print(dict_frame_detail.frame_dict[key].content)
            print(" ")
            print(dict_frame_detail.frame_dict[key].figure)
            print(" ")
            print(dict_frame_detail.frame_dict[key].timestamp)
            print(" ")
            print("-----------------------------------------------------------")
            print("-----------------------------------------------------------")
            print(" ")

    # provide all unique frame details as a dict to create output of the visual content
    @classmethod
    def get_visual_info(cls):
        return dict_frame_detail.frame_dict

    # provide last frame detail to do comparing in text_extraction module to avoid duplication.
    # also avoid giving first frame. because it is main topic
    @classmethod
    def get_last_content(cls):

        if len(dict_frame_detail.frame_dict) < 2:
            return ""

        key = list(dict_frame_detail.frame_dict.keys())[-1]
        # some frames dont have content it contains figure
        if dict_frame_detail.frame_dict[key].content_availability:
            return dict_frame_detail.frame_dict[key].content

        return ""
