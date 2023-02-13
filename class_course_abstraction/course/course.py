from dataclasses import dataclass

@dataclass
class Course:
    name: str
    code: str
    classes_count: str

    def __repr__(self):
        return f"{self.classes_count},{self.code},{self.name}"

    @classmethod
    def init_from_line(cls, line: str):
        class_code, course_code, classroom, building, name, teacher, class_number, classes_count, start, end, weekday_index, parity = line.split(",")
        return Course(name, course_code, classes_count)

