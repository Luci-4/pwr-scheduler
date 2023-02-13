from dataclasses import dataclass

@dataclass
class ClassLocation:
    classroom: str
    building: str

    def __repr__(self):
        return f"{self.classroom},{self.building}"