from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Names:
    id: str
    name: str
    height: int
    date_of_birth: date
    known_for_movies: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.name

    def get_age(self):
        oggi = date.today()
        diff = oggi - self.date_of_birth
        return diff.days