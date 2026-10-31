from dataclasses import dataclass, field


@dataclass
class Genere:
    id: int
    name: str
    ricavo: float
    numeroBrani: int
    clienti: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name