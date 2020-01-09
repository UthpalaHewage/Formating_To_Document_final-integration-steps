"""Pre processing"""
import cv2
import text_contour_detector


class PreProcessor(object):
    """Do the pre-processing for the each image"""
    # create object of the contour detection class
    text_contour_detector_obj = text_contour_detector.TextContourDetector()

    # constructor
    def __init__(self):
        pass

    # method
    def pre_processing(self, image, frame_position, time_stamp):
        """Do the pre-processing task"""
        # convert to grey scale
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # linear contrast stretching
        minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)

        # use sobel-x operation
        sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)

        # threshold
        threshold = cv2.threshold(sobel_img_x, 244, 255, cv2.THRESH_BINARY)[1]

        # Dilation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(11, 2), anchor=(-1, -1))
        img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                                      borderType=cv2.BORDER_REFLECT, borderValue=255)
        # method call
        self.text_contour_detector_obj.contour_detection(img, img_dilate, frame_position, time_stamp)
