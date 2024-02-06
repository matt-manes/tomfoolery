from dataclasses import asdict, dataclass

import dacite
from pathier import Pathier, Pathish
from typing_extensions import Self


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: int


@dataclass
class Calendar:
    num_events: int
    start_month: str
    stop_month: str


@dataclass
class AfraidOfTheDark:
    me: bool
    you: bool


@dataclass
class Venue:
    name: str
    address: Address
    calendar: Calendar
    yee: str
    afraid_of_the_dark: AfraidOfTheDark

    @classmethod
    def load(cls, path: Pathish = Pathier(__file__).parent / "venue.toml") -> Self:
        """Return an instance of this class populated from `path`."""
        data = Pathier(path).loads()
        return dacite.from_dict(cls, data)

    def dump(self, path: Pathish = Pathier(__file__).parent / "venue.toml"):
        """Write the contents of this instance to `path`."""
        data = asdict(self)
        Pathier(path).dumps(data)
