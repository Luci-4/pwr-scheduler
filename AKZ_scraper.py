import requests
from bs4 import BeautifulSoup
from AKZ_scraper_field_query import AKZFieldQuery

from class_course_abstraction.AKZ_class import AKZClass
from class_course_abstraction.class_identifier import ClassIdentifier
from class_course_abstraction.class_location import ClassLocation
from class_course_abstraction.class_time import ClassTime
from class_course_abstraction.class_multi_time import ClassMultiTime
from class_course_abstraction.class_multi_location import ClassMultiLocation
from class_course_abstraction.course.course import Course

class EmptyWeekdayError(Exception): pass

class AKZScraper:
    __URL =  "http://www.akz.pwr.edu.pl/katalog_zap.html"

    @classmethod
    def __get_all_table_rows(cls):
        page = requests.get(cls.__URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all(class_="gradeX")
        return results

    @staticmethod
    def __convert_to_weekday_index(weekday: str) -> int:
        match weekday:
            case "pn":
                return 0
            case "wt":
                return 1
            case "sr":
                return 3
            case "cz":
                return 4
            case "pt":
                return 5
            case "so":
                return 6
            case _:
                assert False, f"fucked up akz weekday with {weekday} argument"

    @classmethod
    def __parse_to_class_time(cls, day_time: str) -> ClassTime:
        open_par_index = day_time.index("(")
        close_par_index = day_time.index(")")
        weekday = day_time[open_par_index+1:close_par_index].strip()
        if not weekday:
            raise EmptyWeekdayError
        parity = ""
        if " " in weekday:
            weekday, parity = weekday.split(" ")
            parity = parity[-1]
        weekday_index = cls.__convert_to_weekday_index(weekday)
        time = day_time[close_par_index+1:].strip()
        start, end = time.split("-")

        class_time = ClassTime(start, end, weekday_index, parity)
        return class_time

    @classmethod
    def __parse_to_class_location(cls, location_str: str) -> ClassLocation:
        space_before_par_index = location_str.index(" (")  
        classroom = location_str[:space_before_par_index].strip()
        building = location_str[space_before_par_index+2:].strip()
        class_location = ClassLocation(classroom, building)
        return class_location

    @classmethod
    def __parse_to_multi_time_and_location(cls, day_time_location: list[str]) -> tuple[ClassTime, ClassLocation]:
        times = []
        locations = []
        day_time_location = day_time_location.split("\n")
        for second_index in range(1, len(day_time_location), 2):
            day_time = day_time_location[second_index-1]
            times.append(cls.__parse_to_class_time(day_time))
            location_str = day_time_location[second_index]
            locations.append(cls.__parse_to_class_location(location_str))
        return ClassMultiTime(times), ClassMultiLocation(locations)

    @classmethod
    def get_classes_by_field_query(cls, field_query: AKZFieldQuery):
        classes = []
        table_rows = cls.__get_all_table_rows()
        for table_row in table_rows:
            course_code, class_code, name, day_time_location, teacher, seats_taken, all_seats, offline, level, _ =[i.get_text(strip=True, separator="\n") for i in table_row.find_all("td")]
            if not (field_query.matches(name, teacher) and level == "I"):
                continue
            class_identifier = ClassIdentifier(class_code,1)
            course = Course(name, course_code, 1)
            try:
                class_multi_time, class_multi_location = cls.__parse_to_multi_time_and_location(day_time_location)
            except EmptyWeekdayError:
                continue

            class_ = AKZClass(teacher,class_identifier,course,class_multi_location, class_multi_time)
            classes.append(class_)
        return classes

