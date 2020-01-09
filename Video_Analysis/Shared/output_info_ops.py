"""here if the frame not contain a subtopic it goes with None in the title field.
create a output for 2nd module"""
import Models.visual_info_output as dict_visual_info


class OutputDictOps(object):
    """class for create dictionary with visual details to second module"""

    def __init__(self):
        pass

    @classmethod
    # get called from frame_seperator module
    def create_dict(cls, visual_info):
        # iterate using key - key is frame position
        for main_key in visual_info:
            # if catch a main topic it should be appear withing before 300 frames
            if not bool(dict_visual_info.output) and main_key < 300:
                # in new dict key of the main topic is a string
                dict_visual_info.output.update({"Main Topic": [visual_info[main_key]]})
            # this is for handle not detecting main topic and put numerical keys to subtopic based content
            elif len(dict_visual_info.output) < 2:
                # when there is not catch a main topic then declare first content frame
                if len(dict_visual_info.output) == 0:
                    dict_visual_info.output.update({1: [visual_info[main_key]]})
                # if there is main topic next one set as 1st
                elif len(dict_visual_info.output) == 1 and list(dict_visual_info.output.keys())[-1] == "Main Topic":
                    dict_visual_info.output.update({1: [visual_info[main_key]]})
                else:
                    previous_values = dict_visual_info.output.get(1)
                    # if there is not a main topic and if 1st subtopic has two or more frame details
                    if previous_values[0].title == visual_info[main_key].title:
                        previous_values.append(visual_info[main_key])
                        dict_visual_info.output.update({1: previous_values})
                    else:
                        # if there is not a main topic then 2nd sub topic is also include here
                        dict_visual_info.output.update({2: [visual_info[main_key]]})
            else:
                # get previous key in the dict
                previous_key = list(dict_visual_info.output.keys())[-1]
                if len(dict_visual_info.output) > 0:

                    values = dict_visual_info.output.get(previous_key)
                    # used to fill content if subtitle is equal to same key
                    if values[0].title == visual_info[main_key].title and previous_key != "Main Topic":
                        values.append(visual_info[main_key])
                        dict_visual_info.output.update({list(dict_visual_info.output.keys())[-1]: values})

                    else:
                        # new frame details with new subtopic key
                        dict_visual_info.output.update({previous_key + 1: [visual_info[main_key]]})
        # print a summary of key with particular frame positions
        file = open("output_text_files/summary.txt", "w+")
        for key in dict_visual_info.output:
            print(key)
            file.write("--------------------------------------------\n\n")
            file.write(str(key) + "\n\n")
            file.write("--------------------------------------------\n\n")
            for values in dict_visual_info.output[key]:
                print(values.frame_position)
                file.write(str(values.frame_position) + "\n\n")
            file.write("############################################\n\n")

            print("-------------------------------")
        file.close()
        # print(dict_visual_info.output)
        # file2 = open("array.txt", "w+")
        # file2.write(str(dict_visual_info.output))
        # file2.close()
        return dict_visual_info.output
