import requests
from bs4 import BeautifulSoup
from akz_scraping.AKZ_query import AKZQuery
from akz_scraping.AKZ_fields import AKZFields

from class_course_abstraction.AKZ_class import AKZClass
from class_course_abstraction.class_identifier import ClassIdentifier
from class_course_abstraction.class_location import ClassLocation
from class_course_abstraction.class_time import ClassTime
from class_course_abstraction.class_multi_time import ClassMultiTime
from class_course_abstraction.class_multi_location import ClassMultiLocation
from class_course_abstraction.course.course import Course

from user_input import user_agreed

class EmptyWeekdayError(Exception): pass

class AKZScraper:
    __URL =  "http://www.akz.pwr.edu.pl/katalog_zap.html"
    __DUMPING_FILE = ".akz-classes.csv"

    @classmethod
    def scrape_all_table_rows(cls) -> None:
        if not user_agreed("updating courses data from www.akz.pwr.edu.pl: confirm action (y/n):"):
            return

        page = requests.get(cls.__URL)
        soup = BeautifulSoup(page.content, "html.parser")
        table_rows = soup.find_all(class_="gradeX")
        if not (table_rows):
            print("www.akz.pwr.edu.pl is not responding")
            return
        cls.__dump_rows_to_file(table_rows)

    @classmethod
    def __dump_rows_to_file(cls, table_rows) -> None:
        contents = ""
        for table_row in table_rows:
            course_code, class_code, name, day_time_location, teacher, seats_taken, all_seats, offline, level, _ =[i.get_text(strip=True, separator="\n") for i in table_row.find_all("td")]
            contents += f"{course_code},{class_code},{name},{day_time_location},{teacher},{seats_taken},{all_seats},{offline},{level}".replace("\n", "\t")
            contents += "\n"

        with open(cls.__DUMPING_FILE, "w+", encoding="utf-8") as file:
            file.write(contents)

    @classmethod
    def __try_to_get_all_rows(cls):
        with open(cls.__DUMPING_FILE, "r", encoding="utf-8") as file:
            rows = [i.strip().split(",") for i in file]
        return rows

    @classmethod
    def __get_all_rows(cls):
        try:
            rows = cls.__try_to_get_all_rows()
            return rows
        except FileNotFoundError:
            cls.scrape_all_table_rows()
            rows = cls.__try_to_get_all_rows()
            return rows

    @staticmethod
    def __convert_to_weekday_index(weekday: str) -> int:
        match weekday:
            case "pn":
                return 0
            case "wt":
                return 1
            case "sr":
                return 2
            case "cz":
                return 3
            case "pt":
                return 4
            case "so":
                return 5
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
        day_time_location = day_time_location.split("\t")
        for second_index in range(1, len(day_time_location), 2):
            day_time = day_time_location[second_index-1]
            times.append(cls.__parse_to_class_time(day_time))
            location_str = day_time_location[second_index]
            locations.append(cls.__parse_to_class_location(location_str))
        return ClassMultiTime(times), ClassMultiLocation(locations)


    @classmethod
    def __matches_with_any_query(cls, queries, found_fields: AKZFields):
        
        for query in queries:
            if query.matches(found_fields):
                return True
        return False

    @classmethod
    def get_classes_by_queries(cls, queries: list[AKZQuery]) -> list:
        classes = []
        rows = cls.__get_all_rows()
        if not rows:
            print("could not find any local AKZ courses data. Try using the scrape_all_table_rows function first")

        for row in rows:
            course_code, class_code, name, day_time_location, teacher, seats_taken, all_seats, offline, level = row
            class_identifier = ClassIdentifier(class_code,1)
            course = Course(name, "WFC" if course_code[:2] == "WF" else "JZC", 1)

            if level != "I":
                continue

            try:
                class_multi_time, class_multi_location = cls.__parse_to_multi_time_and_location(day_time_location)
            except EmptyWeekdayError:
                continue

            found_fields = AKZFields(name=name, teacher=teacher, class_code=class_code, course_code=course_code)

            if not cls.__matches_with_any_query(queries, found_fields):
                continue

            class_ = AKZClass(teacher,class_identifier,course,class_multi_location, class_multi_time)
            classes.append(class_)

        return classes
