from class_course_abstraction.class_location import ClassLocation

class ClassMultiLocation:
    def __init__(self, class_locations: list[ClassLocation]) -> None:
        self.locations = class_locations

    @property
    def buildings_str(self):
            return " ".join([l.building for l in self.locations])

    @property
    def classrooms_str(self):
        return " ".join([l.classroom for l in self.locations])

    def __repr__(self):
        return " ".join([str(l) for l in self.locations])