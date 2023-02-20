from class_course_abstraction.class_identifier import ClassIdentifier
from class_course_abstraction.class_location import ClassLocation
from class_course_abstraction.class_time import ClassTime
from class_course_abstraction.course.course import Course
from class_course_abstraction.class_multi_time import ClassMultiTime
from class_course_abstraction.class_multi_location import ClassMultiLocation

class Class:
    def __init__(
            self, 
            teacher,
            identifier: ClassIdentifier, 
            course: Course, 
            location: ClassLocation | ClassMultiLocation,
            time: ClassTime | ClassMultiTime
        ) -> None:
        self.teacher = teacher
        self.identifier = identifier
        self.course = course
        self.location = location
        self.time = time
        self.score = 0

    def __repr__(self) -> str:
        return f"{self.course},{self.identifier},{self.teacher},{self.time}"

    @property
    def code(self):
        return self.identifier.code

    @property
    def classroom(self):
        return self.location.classroom

    @property
    def building(self):
        return self.location.building

    @property
    def time_bounds(self):
        return self.time.start, self.time.end 

    def collides(self, other):
        return self.time.collides(other.time)

    def deep_get_attribute(self, query):
        consecutive_attributes = query.split(".")
        obj = self
        for attr in consecutive_attributes:
            obj = getattr(obj, attr)

        return obj

    @property
    def score_attributes_dict(self):
        return {
            "teacher": self.teacher,
            "building": self.location.building,
            "classroom": self.location.classroom,
            "hour": f"{self.time.start_str}-{self.time.end_str}",
            "day": self.time.weekday
        }

    def get_score_attrs_values_with_identifier(self, fields):
        return [str(self.identifier.code)]+[self.score_attributes_dict[field] for field in fields]
        
    @staticmethod
    def sort_callback_by_code(class_):
        code = class_.identifier.code
        after_dash = code[code.index('-'):]
        code_number = int("".join([i for i in after_dash if i.isnumeric()]))
        return ord(code[-1].lower())/ord('z') + code_number 

    @classmethod
    def init_from_line(cls, line: str):
        class_code, course_code, classroom, building, name, teacher, class_number, classes_count, start, end, weekday_index, parity = line.split(",")
        class_identifier = ClassIdentifier(class_code, class_number)
        course = Course(name, course_code, classes_count)
        location = ClassLocation(classroom, building)
        time = ClassTime(start, end, weekday_index, parity)

        return Class(teacher, class_identifier, course, location, time)
