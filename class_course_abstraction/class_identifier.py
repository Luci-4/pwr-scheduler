from dataclasses import dataclass

@dataclass
class ClassIdentifier:
    code: str
    number: str

    def __repr__(self):
        return f"{self.code},{self.number}"
