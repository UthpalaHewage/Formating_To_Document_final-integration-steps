"""To detect the figures without clear borders"""
import cv2
import text_extraction
import Shared.frame_dict_ops as ops


# method
def pre_process_image(img):
    """Do pre-processing for the frame"""
    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)
    # Sobel
    sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)
    # threshold
    threshold = cv2.threshold(sobel_img_x, 96, 255, cv2.THRESH_BINARY)[1]
    # Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(14, 3), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=3,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)

    return img_dilate


# method
def find_text_boxes(pre, min_text_height_limit=15, max_text_height_limit=60):
    """Find text box contours"""
    # Looking for the text spots contours
    contours = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

    # Getting the texts bounding boxes based on the text size assumptions
    boxes = []
    # iterate selected contours to create rect
    for contour in contours:
        box = cv2.boundingRect(contour)
        h = box[3]
        # select relevant contours
        if min_text_height_limit < h < max_text_height_limit:
            boxes.append(box)

    return boxes


# method
def find_table_in_boxes(boxes, min_columns=2):
    """detect table from text boxes"""
    rows = {}
    cols = {}

    # Clustering the bounding boxes by their positions
    for box in boxes:
        (x, y, w, h) = box
        # cell_threshold
        col_key = x
        # cell_threshold
        row_key = y
        cols[row_key] = [box] if col_key not in cols else cols[col_key] + [box]
        rows[row_key] = [box] if row_key not in rows else rows[row_key] + [box]

    # Filtering out the clusters having less than 2 cols
    table_cells = list(filter(lambda r: len(r) >= min_columns, rows.values()))
    # Sorting the row cells by x coord
    table_cells = [list(sorted(tb)) for tb in table_cells]
    # Sorting rows by the y coord
    table_cells = list(sorted(table_cells, key=lambda r: r[0][1]))

    return table_cells


# method
def build_lines(table_cells):
    """Generate lines in the table"""
    if table_cells is None or len(table_cells) <= 0:
        return [], []

    max_last_col_width_row = max(table_cells, key=lambda b: b[-1][2])
    max_x = max_last_col_width_row[-1][0] + max_last_col_width_row[-1][2]

    max_last_row_height_box = max(table_cells[-1], key=lambda b: b[3])
    max_y = max_last_row_height_box[1] + max_last_row_height_box[3]

    hor_lines = []
    ver_lines = []

    for box in table_cells:
        x = box[0][0]
        y = box[0][1]
        hor_lines.append((x, y, max_x, y))

    for box in table_cells[0]:
        x = box[0]
        y = box[1]
        ver_lines.append((x, y, x, max_y))

    (x, y, w, h) = table_cells[0][-1]
    ver_lines.append((max_x, y, max_x, max_y))
    (x, y, w, h) = table_cells[0][0]
    hor_lines.append((x, max_y, max_x, max_y))

    return hor_lines, ver_lines


# method
def get_main_points(hor_lines, ver_lines):
    """get point to crop around the figure"""
    final_box = []
    # select suitable vertical lines
    if len(ver_lines) > 2 and not ver_lines[0][3] - ver_lines[0][1] < 150:
        final_box.append(ver_lines[0])
        final_box.append(ver_lines[len(ver_lines) - 1])
    # select suitable horizontal lines
    if len(hor_lines) > 2 and len(final_box) != 0 and not (hor_lines[0][2] - hor_lines[0][0] < 150):
        final_box.append(hor_lines[0])
        final_box.append(hor_lines[len(hor_lines) - 1])

    else:
        return [-100, -100, -100, -100]
    # put default values to variable
    min_x = 2000000
    min_y = 2000000
    max_x = -1
    max_y = -1
    # select min and max point to draw rectangle around the figure
    if len(final_box) == 4:
        for line in final_box:
            [x1, y1, x2, y2] = line

            if min_x > x1:
                min_x = x1
            if min_x > x2:
                min_x = x2
            if max_x < x1:
                max_x = x1
            if max_x < x2:
                max_x = x2

            if min_y > y1:
                min_y = y1
            if min_y > y2:
                min_y = y2
            if max_y < y1:
                max_y = y1
            if max_y < y2:
                max_y = y2

        return [min_x, min_y, max_x, max_y]


class FigureDetectorBorderless(object):
    """class for detect figures from above methods"""
    # create object of text extraction class
    text_extraction_obj = text_extraction.TextExtraction()
    # create object of frame detail operation class
    ops_obj = ops.DictOps()

    # constructor
    def __init__(self):
        self.first = True
        self.previous_h = 0
        self.previous_w = 0

    # method - for other methods and finalize frame with borderless figures
    def figure_detection_borderless(self, gray_img, binary_img, frame_position, time_stamp, contours_list_title):

        img = gray_img.copy()

        width = gray_img.shape[1]
        # method call
        pre_processed = pre_process_image(img)
        # method call
        text_boxes = find_text_boxes(pre_processed)
        # method call
        cells = find_table_in_boxes(text_boxes)
        # method call
        hor_lines, ver_lines = build_lines(cells)
        # method call
        [min_x, min_y, max_x, max_y] = get_main_points(hor_lines, ver_lines)
        # select frames without borderless figures
        if min_x == -100 and min_y == -100 and max_x == -100 and max_y == -100:
            # method call
            self.text_extraction_obj.extract_text_string(binary_img, frame_position, time_stamp, contours_list_title)
        else:
            if self.first:
                # save cropped figure to table directory
                cv2.imwrite("figures/" + str(frame_position) + ".jpg",
                            gray_img[min_y:max_y, min_x:max_x])

                self.first = False
                self.previous_h = max_y - min_y
                self.previous_w = max_x - min_x
                # add details to frame details dictionary
                # method call
                self.ops_obj.add_to_dict_from_figure(frame_position, time_stamp)
                # method call - to get text around the figure
                self.text_extraction_obj.extract_text_string(binary_img[0:min_y, 0:width], frame_position, time_stamp,
                                                             contours_list_title)

            else:
                # select unique figures
                if self.previous_w == max_x - min_x or self.previous_h == max_y - min_y:
                    # values with above not consider as a figure
                    pass
                else:
                    # save cropped figure to table directory
                    cv2.imwrite("figures/" + str(frame_position) + ".jpg",
                                gray_img[min_y:max_y, min_x:max_x])
                    self.previous_h = max_y - min_y
                    self.previous_w = max_x - min_x
                    # add details to frame details dictionary
                    # method call
                    self.ops_obj.add_to_dict_from_figure(frame_position, time_stamp)
                    # method call - to get text around the figure
                    self.text_extraction_obj.extract_text_string(binary_img[0:min_y, 0:width], frame_position,
                                                                 time_stamp, contours_list_title)
