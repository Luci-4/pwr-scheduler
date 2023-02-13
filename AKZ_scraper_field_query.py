from dataclasses import dataclass

@dataclass
class AKZFieldQuery:
    name: str = None
    teacher: str = None

    def matches(self, name: str, teacher: str):
        if self.name and self.teacher:
            return self.name.lower() in name.lower() and self.teacher.lower() in teacher.lower()

        if self.name and self.name.lower() in name.lower():
            return True

        if self.teacher and self.teacher.lower() in teacher.lower():
            return True

        return False 


