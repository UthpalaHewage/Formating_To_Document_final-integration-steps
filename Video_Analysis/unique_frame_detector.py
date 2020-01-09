"""This module is use identify unique frames from the video"""
import cv2
import border_figure_detector


class UniqueFrameDetector(object):
    """class for the detecting unique frame"""
    # object of border_figure_detector_class
    border_figure_detector_obj = border_figure_detector.FigureDetectorBorder()

    # constructor
    def __init__(self):
        self.previous_image = None
        self.first_frame = False
        self.skip_count_by_size = 0
        self.skip_count_by_pixel = 0

    # method
    def detect_unique(self, img, img_empty, height, frame_position, time_stamp, max_width, max_width_x, title_image):
        """detect unique frame using localize text"""
        # to be a suitable frame, max_width of a contour in a frame should larger than 180
        if max_width > 180:
            # check is this the first selected frame and set first values for previous_image
            if not self.first_frame:
                self.first_frame = True
                # crop text area using max_width and x value of max_width
                crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
                self.previous_image = crop_img

            else:
                # crop text area using max_width and x value of max_width
                crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
                # check dimensions of previous and current text regions
                if self.previous_image.shape == crop_img.shape:
                    # to avoid blur effect when changes the frames
                    self.skip_count_by_pixel += 1
                    if self.skip_count_by_pixel > 50:

                        self.skip_count_by_pixel = 0
                        self.skip_count_by_size = 0
                        # get number of pixels of value 255
                        previous_image_none_zero_px = cv2.countNonZero(self.previous_image)
                        current_image_none_zero_pixel = cv2.countNonZero(crop_img)

                        height1, width1 = self.previous_image.shape
                        height2, width2 = crop_img.shape
                        # get number of pixels of value 255 - black pixels - text pixels
                        previous_image_zero_px = height1 * width1 - previous_image_none_zero_px
                        current_image_zero_px = height2 * width2 - current_image_none_zero_pixel

                        x_ = previous_image_zero_px + 75
                        y_ = previous_image_zero_px - 75
                        # to check changes inside same dimension text regions
                        if x_ < current_image_zero_px or y_ > current_image_zero_px:
                            self.previous_image = crop_img
                            # save binary and grey image in image directory
                            cv2.imwrite("image/" + str(frame_position - 50) + "-Pixel" + ".jpg", img)
                            cv2.imwrite("image/" + str(frame_position - 50) + "_2-Pixel" + ".jpg", img_empty)
                            # method call
                            self.border_figure_detector_obj.figure_detection_border(img, img_empty,
                                                                                    frame_position - 50, time_stamp,
                                                                                    title_image)
                # dimension are different in previous and current text region
                else:
                    # to avoid blur effect when changes the frames
                    self.skip_count_by_size += 1

                    if self.skip_count_by_size > 50:
                        self.skip_count_by_pixel = 0
                        self.skip_count_by_size = 0

                        self.previous_image = crop_img
                        # save binary and grey image in image directory
                        cv2.imwrite("image/" + str(frame_position - 50) + "-Size" + ".jpg", img)
                        cv2.imwrite("image/" + str(frame_position - 50) + "_2-size" + ".jpg", img_empty)
                        # method call
                        self.border_figure_detector_obj.figure_detection_border(img, img_empty,
                                                                                frame_position - 50, time_stamp,
                                                                                title_image)
        cv2.imshow("video", img)
