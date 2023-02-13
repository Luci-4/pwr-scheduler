from datetime import datetime

class ClassTime:
    def __init__(self, start: str, end: str, weekday_index: str, week_parity: str) -> None:
        self.start = datetime.strptime(start,"%H:%M")
        self.end = datetime.strptime(end,"%H:%M")
        self.weekday_index = int(weekday_index)
        self.week_parity = week_parity

    def collides(self, other):
        if isinstance(other, ClassTime):
            return self.__collides_with_class_time(other)
        return self.__collides_with_multi_time(other)

    def __collides_with_multi_time(self, other):
        return other.collides(self)
    
    def __collides_with_class_time(self, other):
        
        week_parity_1 = self.week_parity
        week_parity_2 = other.week_parity
        weekday_1 = self.weekday_index
        weekday_2 = other.weekday_index
        start1, end1 = self.start, self.end
        start2, end2 = other.start, other.end
        
        parity_is_invalid = (bool(week_parity_1) ^ bool(week_parity_2)) or week_parity_1== week_parity_2
        if weekday_1 == weekday_2 and parity_is_invalid:

            if start1 <= end2 and end1 >= start2:
                return True

        return False

    @property
    def start_str(self):
        return datetime.strftime(self.start,'%H:%M')

    @property
    def end_str(self):
        return datetime.strftime(self.end,'%H:%M')

    def __repr__(self):
        return f"{self.start},{self.end},{self.weekday_index},{self.week_parity}"

    @property
    def weekday(self):
        match str(self.weekday_index):
            case "0":
                return "Pn"
            case "1":
                return "Wt"
            case "2":
                return "Sr"
            case "3":
                return "Czw"
            case "4":
                return "Pt"
            case "5":
                return "Sob"
            case "6":
                return "Nd"
            case _:
                assert False, "Wrong weekday index fucker"