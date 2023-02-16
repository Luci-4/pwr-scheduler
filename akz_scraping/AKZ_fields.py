from dataclasses import dataclass

@dataclass
class AKZFields:
    class_code: str = ""
    course_code: str = ""
    name: str = ""
    teacher: str = ""

    def __post_init__(self):
        self.values = [
            self.class_code,
            self.course_code,
            self.name,
            self.teacher
        ]
    