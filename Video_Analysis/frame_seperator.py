"""Separating Frames"""
import cv2
import pre_processor
import Shared.frame_dict_ops as ops
import Shared.output_info_ops as output_ops
import Models.gui_component as container
import doc_formatting as doc_ops


class FrameSeperator(object):
    """This class do the separating video into frames"""
    # create the object of pre_processor module
    pre_processor_obj = pre_processor.PreProcessor()
    # create object of frame detail operation class(not the output dict)
    ops_obj = ops.DictOps()
    # create the object of the output dict
    output_ops_obj = output_ops.OutputDictOps()

    # constructor
    def __init__(self):
        pass

    def catch_video(self, video_location):
        """first method get call from GUI"""
        # change the progress bar values
        container.component[1]['value'] = 10
        container.component[0].update_idletasks()
        # get the video
        cap = cv2.VideoCapture(video_location)
        # get frame rate
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # method call
        self.seperator(cap)

    # method
    def seperator(self, cap):
        """This method do separation task"""
        if not cap.isOpened():
            print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
        # get first frame of the video as 1
        frame_position = 1

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                # get timestamp of current frame
                time_stamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                # sent frame to pre-processing
                self.pre_processor_obj.pre_processing(frame, frame_position, time_stamp)
                # track frame position
                frame_position += 1
                # condition for hard stop the separating to frames
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                # method call - to print just frame details(not output dict)
                self.iterate_different_frame_timestamp()
                print("################################################")
                # get frame info to variable
                output_visual_info = self.ops_obj.get_visual_info()
                # pass frame details to creat output visual info dict
                visual_output = self.output_ops_obj.create_dict(output_visual_info)
                print("-----------------------Write To Doc-------------------------")
                doc_ops.write_to_doc_method(visual_output)
                print("-----------------------Write To Doc-------------------------")
                # change the progress bar values
                container.component[1]['value'] = 50
                container.component[0].update_idletasks()
                break
        cap.release()

    # method
    def iterate_different_frame_timestamp(self):
        """Iterate selected frame's details"""
        # method call - to print just frame details(not output dict)
        self.ops_obj.view_dict()
