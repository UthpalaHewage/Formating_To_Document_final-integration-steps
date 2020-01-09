"""Detect tables diagrams with have clear borders"""
import cv2
import text_extraction
import Shared.frame_dict_ops as ops
import borderless_figure_detector


class FigureDetectorBorder(object):
    """class for detect figures"""
    # create object of text extraction class
    text_extraction_obj = text_extraction.TextExtraction()
    borderless_figure_detector_obj = borderless_figure_detector.FigureDetectorBorderless()
    # create object of frame detail operation class
    ops_obj = ops.DictOps()

    # constructor
    def __init__(self):
        self.first = True
        self.previous_h = 0
        self.previous_w = 0

    # method
    def figure_detection_border(self, gray_img, binary_img, frame_position, time_stamp, contours_list_title):
        """method for detect borders"""
        img = gray_img.copy()
        height, width = gray_img.shape
        #         # edge detection
        edges = cv2.Canny(img, 31, 180, apertureSize=3)
        # contour detection
        contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        # default values
        table_x = -1
        table_y = -1
        # minimum values that a figure can have
        table_w = 450
        table_h = 200

        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)
            # Don't plot small false positives that aren't text
            if w > table_w and h > table_h:
                table_x = x
                table_y = y
                table_h = h
                table_w = w
        if not table_x == -1 and not table_y == -1 and not table_h > height - 50:

            if self.first:
                # save cropped figure
                cv2.imwrite("figures/" + str(frame_position) + ".jpg",
                            gray_img[table_y:table_y + table_h, table_x:table_x + table_w])

                self.first = False
                self.previous_h = table_h
                self.previous_w = table_w
                # add details to frame details dictionary
                # method call
                self.ops_obj.add_to_dict_from_figure(frame_position, time_stamp)
                # method call - to get text around the figure
                self.text_extraction_obj.extract_text_string(binary_img[0:table_y, 0:width], frame_position, time_stamp,
                                                             contours_list_title)

            else:
                if self.previous_w == table_w or self.previous_h == table_h:
                    # this scenario is not valid for detect relevant borders
                    pass
                else:
                    # save cropped figure
                    cv2.imwrite("figures/" + str(frame_position) + ".jpg",
                                gray_img[table_y:table_y + table_h, table_x:table_x + table_w])

                    self.previous_h = table_h
                    self.previous_w = table_w
                    # add details to frame details dictionary
                    # method call
                    self.ops_obj.add_to_dict_from_figure(frame_position, time_stamp)
                    # method call - to get text around the figure
                    self.text_extraction_obj.extract_text_string(binary_img[0:table_y, 0:width], frame_position,
                                                                 time_stamp, contours_list_title)
        else:
            # method call
            self.borderless_figure_detector_obj.figure_detection_borderless(gray_img, binary_img,
                                                                            frame_position, time_stamp,
                                                                            contours_list_title)
