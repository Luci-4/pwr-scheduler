import os
from class_course_abstraction.class_ import Class
from class_course_abstraction.class_time import ClassTime
from class_course_abstraction.class_location import ClassLocation
from class_course_abstraction.AKZ_class import AKZClass


class Timetable:
    YAML_DIR = "output/yaml"
    PDF_DIR = "output/timetables"
    def __init__(self, classes) -> None:
        self.classes = classes

    @classmethod
    def create_output_folders(cls):
        os.mkdir(cls.YAML_DIR)
        os.mkdir(cls.PDF_DIR)

    @staticmethod
    def __remove_all_files_from_dir(dirname: str):
        for f in os.listdir(dirname):
            os.remove(os.path.join(dirname, f))

    @classmethod
    def clear_output_folders(cls):
        cls.__remove_all_files_from_dir(cls.YAML_DIR)
        cls.__remove_all_files_from_dir(cls.PDF_DIR)

    @staticmethod
    def assign_color(class_format):
        match class_format.lower():
            case "w":
                return "#FCE1E4"[1:]
            case "l":
                return "#DAEAF6"[1:]
            case "c":
                return "#FCF4DD"[1:]
            case _:
                return "#FFFFFF"[1:]

    def format_weekday(self, weekday_index):
        match int(weekday_index):
            case 0:
                return "M"
            case 1:
                return "T"
            case 2:
                return "W"
            case 3:
                return "H"
            case 4:
                return "F"
            case 5:
                return "Sat"
            case _:
                raise Exception("you fucking dumbass invalid weekday index")

    def __format_class(self, class_: Class | AKZClass, time: ClassTime = None, location: ClassLocation = None):
            if time is None:
                time = class_.time
            if location is None:
                location = class_.location

            start, end = time.start, time.end
            delta = end - start
            # print(course.start.strftime("%H:%M"), course.end.strftime("%H:%M"))
            match time.week_parity.lower():
                case "n":
                    formated_start_str = start.strftime("%H:%M")
                    formated_end_str = (end-delta/2).strftime("%H:%M")

                case "p":
                    formated_start_str = (start+delta/2).strftime("%H:%M")
                    formated_end_str = end.strftime("%H:%M")
                case _:
                    formated_start_str = start.strftime("%H:%M")
                    formated_end_str = end.strftime("%H:%M")
            # print(delta, formated_start_str, formated_end_str)
            # print(20*"*")

            class_entry = f"""- name: {class_.code} {class_.course.code} {class_.course.name} {class_.teacher} {location.classroom} {location.building} {start.strftime("%H:%M")}
  days: {self.format_weekday(time.weekday_index)}
  time: {formated_start_str} - {formated_end_str}
  color: \"{self.assign_color(class_.course.code[-1])}\"\n\n"""
            class_entry = "".join([self.convert_to_latin(i) for i in class_entry])
            return class_entry


    def dump(self, index, score):
        entry = ""
        for class_ in self.classes:
            
            if isinstance(class_, AKZClass):
                class_entry = ""
                for time, location in zip(class_.time.times, class_.location.locations):

                    class_entry += self.__format_class(class_, time, location)
            elif isinstance(class_, Class):
                class_entry = self.__format_class(class_)

            entry += class_entry
        file_name = f"schedule{index}-{int(score)}score"
        with open(f"{self.YAML_DIR}/{file_name}.yaml", "w+") as file:
            file.write(entry)
        os.chdir(os.getcwd())
        os.system(f"pdfschedule --start-monday {self.YAML_DIR}/{file_name}.yaml {self.PDF_DIR}/{file_name}.pdf")

    @staticmethod
    def convert_to_latin(char: str) -> str:
        is_upper = char.isupper()
        result = ""
        match char.lower():
            case "à" | "â" | "á" | "å" | "ä" | "ã" | "ą" | "æ":
                result = "a"

            case "ç" | "ĉ" | "ć" | "č":
                result = "c"

            case "ď" |"ð":
                result = "d"

            case "è" | "é" |  "ê" | "ë" | "ę" | "ě":
                result = "e"

            case "ĝ" | "ğ":
                result = "g"

            case "ĥ":
                result = "h"
            
            case "î" | "ì" | "í" | "ï" | "ı":
                result = "i"

            case "ĵ":
                result = "j"

            case "ł" | "ľ":
                result = "l"
            
            case "ñ" | "ń" | "ň":
                result = "n"
            
            case "œ" | "ò" | "ö" | "ô" | "ó" | "õ" | "ø":
                result = "o"

            case "ř":
                result = "r"
            
            case "ŝ" | "ş" | "ś" | "š" | "ß":
                result = "s"
            
            case "ť" | "þ":
                result = "t"
            
            case "ù" | "ú" | "û" | "ŭ" | "ü" | "ů":
                result = "u"

            case "ý":
                result = "y"
            
            case "ź" | "ż" | "ž":
                result = "z"
            
            case _:
                result = char
        if is_upper:
            return result.upper()
        return result