from dataclasses import dataclass

@dataclass
class CourseIdentifier:
    code: str
    classes_count: str

    def __repr__(self):
        return f"{self.classes_number},{self.code}"