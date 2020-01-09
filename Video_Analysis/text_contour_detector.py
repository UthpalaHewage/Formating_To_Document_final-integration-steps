"""Contours Detection"""
import cv2
import numpy as np
import unique_frame_detector


class TextContourDetector(object):
    "This find the contour of the each frame"
    # object of unique frame detector class
    obj = unique_frame_detector.UniqueFrameDetector()

    # constructor
    def __init__(self):
        pass

    # method - detect contours in pre-processed frame and select suitable contours for text
    def contour_detection(self, img, img_dialate, frame_position, time_stamp):
        """Do the detecting of rect contours for the given constraints"""
        # get measurements of the image
        height, width = img.shape
        # Find Contours
        # simply  as a curve joining all the continuous points
        contours = cv2.findContours(img_dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        # keep the selected non-title contours
        contours_list = []
        # keep contours related to sub-title for large font size
        title_large = []
        # keep contours related to sub-title for small font size
        title_small = []
        # max width of the selected contours for the selected frame
        max_width = 0
        # x coord for the max width rect contour
        max_width_x = 0

        for contour in contours:
            # Calculates the up-right bounding rectangle of a point set
            # brect = (x,y,w,h)
            brect = cv2.boundingRect(contour)
            # compare w/h ratio
            ar = brect[2] / brect[3]

            # localize text based on following conditions
            # 2->w 3->h
            if ar >= 2.7 and brect[2] >= 40 and 17 <= brect[3] <= 60:

                if 35 < brect[3] and (brect[1] + brect[3]) < ((height / 3) + 100):
                    if 36 < brect[3]:
                        title_large.append(brect)
                    else:
                        title_small.append(brect)
                else:
                    contours_list.append(brect)
                # catch width and x value of widest rectangle in the particular frame
                if max_width < brect[2]:
                    max_width = brect[2]
                    max_width_x = brect[0]
        # contain the selected sub-title contours
        selected_title = []
        if len(title_large) == 0:
            selected_title = title_small
        else:
            selected_title = title_large
            contours_list = contours_list + title_small
        # select the true contours of the sub-title
        true_title = []
        if len(selected_title) != 0:
            title_min_x = 200000
            title_min_y = 200000
            max_h = 0

            for x, y, w, h in selected_title:
                if x < title_min_x:
                    title_min_x = x
                if y < title_min_y:
                    title_min_y = y
                if max_h < y + h:
                    max_h = y + h

            true_title = [(title_min_y - 10, max_h + 10, title_min_x - 10, width)]

        # method call
        self.separate_contour(img, contours_list, max_width, max_width_x, frame_position, time_stamp,
                              true_title)

    # method
    def separate_contour(self, img, contours_list, max_width, max_width_x, frame_position, time_stamp,
                         contours_list_title):
        """ Mark selected contour in blank image"""
        # get height and width of current frame
        height, width = img.shape
        # create a blank image using dimension of frame to store content get from contour
        img_empty_content = 255 * np.ones([height, width], dtype=np.uint8)
        # create a blank image using dimension of frame to store sub-title get from contour
        img_empty_title = 255 * np.ones([height, width], dtype=np.uint8)
        # method call
        content_image = self.set_text(img, img_empty_content, contours_list, False)
        # method call
        title = self.set_text(img, img_empty_title, contours_list_title, True)
        # method call
        self.obj.detect_unique(img, content_image, height, frame_position, time_stamp, max_width, max_width_x,
                               title)

    def set_text(self, img, img_empty, contours_list, tag):
        """Set localize text into blank image-so now no effect of person"""
        # iterate given contours
        for r in contours_list:
            # do suitable cropping for content and sub-title
            if tag:

                blur = cv2.GaussianBlur(img[r[0]:r[1], r[2]:r[3]], (3, 3), 0)
            else:
                blur = cv2.GaussianBlur(img[r[1] - 10:r[1] + r[3] + 20, r[0] - 10:r[0] + r[2] + 20], (3, 3), 0)
            # pre-processing for localized text
            threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)
            kernel = np.ones((1, 1), np.uint8)
            img_dilate = cv2.dilate(threshold, kernel, iterations=1)
            img_erode = cv2.erode(img_dilate, kernel, iterations=1)
            # set to blank image with correct place
            if tag:
                img_empty[r[0]:r[1], r[2]:r[3]] = img_erode
            else:
                img_empty[r[1] - 10:r[1] + r[3] + 20, r[0] - 10:r[0] + r[2] + 20] = img_erode

        return img_empty
