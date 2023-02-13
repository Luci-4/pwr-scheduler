from class_course_abstraction.class_identifier import ClassIdentifier
from class_course_abstraction.course.course import Course
from class_course_abstraction.class_multi_time import ClassMultiTime
from class_course_abstraction.class_multi_location import ClassMultiLocation
from class_course_abstraction.class_ import Class

class AKZClass(Class):
    def __init__(self, teacher, identifier: ClassIdentifier, course: Course, location: ClassMultiLocation, time: ClassMultiTime) -> None:
        super().__init__(teacher.replace("\n", " "), identifier, course, location, time)

    @property
    def time_bounds(self):
        return [(t.start, t.end) for t in self.time.times]

    @property
    def score_attributes_dict(self):
        return {
            "teacher": self.teacher,
            "building": self.location.buildings_str,
            "classroom": self.location.classrooms_str,
            "hour": " ".join([f"{start}-{end}" for (start, end) in self.time.times_bounds_in_str]),
            "day": " ".join(self.time.weekdays)
        }

    @classmethod
    def init_from_line(cls, line: str):
        raise NotImplementedError