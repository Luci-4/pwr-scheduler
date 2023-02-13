from class_course_abstraction.class_ import Class
import itertools
import os
from timetable import Timetable

class Schedule:
    def __init__(self, classes: list[Class], emergent_scoring_callbacks=None) -> None:
        self.classes = classes
        if emergent_scoring_callbacks is None:
            emergent_scoring_callbacks = []
        self.__emergent_scoring_callbacks = emergent_scoring_callbacks
        self.timetable = Timetable(classes)
    
    @property
    def class_codes(self):
        return [c.code for c in self.classes]
    
    def dump_to_timetable(self, index: int):
        self.timetable.dump(index, self.score)

    def display_planned_schedule(self,ind: int):
        for i in sorted(self.classes, key=lambda x: x.identifier.code):
            if i.course.code[-1] == "W":
                print(i)
        print()
        for i in sorted(self.classes, key=lambda x: x.identifier.code):
            if i.course.code[-1] != "W":
                print(i)

        print(ind)
        print(self.score)
        print(20*"-")

    @property
    def __additional_emergent_score(self):
        sum_ = 0
        for callback_ in self.__emergent_scoring_callbacks:
            sum_ += callback_(self.classes)
        return sum_
            

    @property
    def score(self):
        # for i in sorted(self.classes, key=lambda x: int(x.code[-2:-4:-1])):
        #     print(i.code, i.score)
        return sum([i.score for i in self.classes])
