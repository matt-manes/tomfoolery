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
class YeeHaw:
    yeehaw: bool


@dataclass
class Venue:
    name: str
    address: Address
    calendar: Calendar
    yeehaw: YeeHaw

    @classmethod
    def load(cls, path: Pathish = Pathier(__file__).parent / "venue.toml") -> Self:
        """Return a `datamodel` object populated from `path`."""
        data = Pathier(path).loads()
        return dacite.from_dict(cls, data)

    def dump(self, path: Pathish = Pathier(__file__).parent / "venue.toml"):
        """Write the contents of this `datamodel` object to `path`."""
        data = asdict(self)
        Pathier(path).dumps(data)

    def howdy(self):
        print("yeehaw")
