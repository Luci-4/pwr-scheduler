from dataclasses import dataclass

@dataclass
class AKZFieldQuery:
    name: str = None
    teacher: str = None

    def matches(self, name: str, teacher: str):
        if self.name and self.teacher:
            return self.name in name and self.teacher in teacher

        if self.name and self.name in name:
            return True

        if self.teacher and self.teacher in teacher:
            return True

        return False 


