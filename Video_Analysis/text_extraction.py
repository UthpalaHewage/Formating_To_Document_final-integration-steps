"""Extract text as string for given region"""
import re
import pytesseract
import Shared.frame_dict_ops as ops

# for use ocr library
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class TextExtraction(object):
    """Extract text as string"""
    # add details to frame details dictionary
    # method call
    ops_obj = ops.DictOps()

    # constructor
    def __init__(self):
        self.first = True
        self.previous_content = None

    # method
    def extract_text_string(self, content_image, frame_position, time_stamp, title_img):
        """using ocr library get the text content of the image"""
        # extract title as string
        title = pytesseract.image_to_string(title_img, lang='eng')
        title = title.replace("\n", " ")
        # extraction content of the frame
        content = pytesseract.image_to_string(content_image, lang='eng')

        # content should have at least 4 characters
        if len(content) > 4:
            # method call - pre process content to compare with previous content and for remove duplication of frames
            self.string_manipulation(content.strip(), frame_position, time_stamp, title)
        # regions which have only title
        elif len(content) < 4 and len(title) > 3:
            # method call
            self.write_to_text_file("", frame_position, time_stamp, title)

    # method - identify similar frame content to identify unique content frame
    def string_manipulation(self, content, frame_position, time_stamp, title):
        # if this is the first content frame
        if self.first:
            # method call
            self.write_to_text_file(content, frame_position, time_stamp, title)
            self.first = False
            self.previous_content = content
        else:
            # do preprocess compare only using alphabetic characters
            previous_trim_content = "".join(re.findall("[a-zA-Z]+", self.previous_content.lower()))
            current_trim_content = "".join(re.findall("[a-zA-Z]+", content.lower()))
            # compare with previous frame content - for remove duplication of frames
            if previous_trim_content != current_trim_content:
                # method call
                self.previous_content = content
                # method call
                self.write_to_text_file(content, frame_position, time_stamp, title)

    # method
    def write_to_text_file(self, content, frame_position, time_stamp, title):
        """write to content to a text file"""
        # removing repeating lines
        new_content = self.remove_repeating_content(content)
        # write to file  - file name is frame position
        file = open("output_text_files/"+str(frame_position) + ".txt", "w+")
        file.write("------------------------------------------------\n\n")
        file.write(str(time_stamp))
        file.write("\n\n------------------------------------------------\n\n")
        file.write(title)
        file.write("\n\n------------------------------------------------\n\n")
        file.write(new_content)
        file.write("\n\n------------------------------------------------\n\n")
        file.close()
        # add details to frame details dictionary
        # change parameters according to frame content
        if len(title) == 0 and len(new_content) != 0:
            # method call
            self.ops_obj.add_to_dict_from_text_extract(frame_position, False, None, True, new_content, time_stamp)
        elif len(title) != 0 and len(new_content) == 0:
            # method call
            self.ops_obj.add_to_dict_from_text_extract(frame_position, True, title, False, None, time_stamp)
        else:
            # method call
            self.ops_obj.add_to_dict_from_text_extract(frame_position, True, title, True, new_content, time_stamp)

    def remove_repeating_content(self, content):
        """repeating content from adjacent frames"""

        previous_content = self.ops_obj.get_last_content()

        if previous_content == "":
            return content

        previous_content = list(previous_content.split("\n"))
        current_content = list(content.split("\n"))
        # compare previous content line by line
        for line in previous_content:
            if line in current_content:
                current_content.remove(line)

        new_content = "\n".join(current_content)
        return new_content.strip()
