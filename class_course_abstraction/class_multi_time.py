from class_course_abstraction.class_time import ClassTime
import itertools

class ClassMultiTime:
    def __init__(self, class_times: list[ClassTime]) -> None:
        self.times = class_times

    @property
    def times_bounds_in_str(self) -> list[tuple[str, str]]:
        return [(t.start_str, t.end_str) for t in self.times]

    @property
    def weekdays(self):
        return [t.weekday for t in self.times]

    def collides(self, other):
        if isinstance(other, ClassTime): 
            return self.__collides_with_class_time(other)
        time_pairs = list(itertools.product(self.times, other.times))
        for time1, time2 in time_pairs:
            if time1.collides(time2) or time2.collides(time1):
                return True
        return False

    def __collides_with_class_time(self, other: ClassTime):
        for time in self.times:
            if time.collides(other):
                return True
        return False


    def __repr__(self):
        result = ""
        for time in self.times:
            result += f"{time} "
        return result
    
