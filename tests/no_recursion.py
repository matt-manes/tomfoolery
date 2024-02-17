from dataclasses import asdict, dataclass

import dacite
from pathier import Pathier, Pathish
from typing_extensions import Self


@dataclass
class Venue:
    name: str
    address: dict[str, str]
    calendar: dict[str, str]

    @classmethod
    def load(cls, path: Pathish = Pathier(__file__).parent / "venue.toml") -> Self:
        """Return an instance of this class populated from `path`."""
        data = Pathier(path).loads()
        return dacite.from_dict(cls, data)

    def dump(self, path: Pathish = Pathier(__file__).parent / "venue.toml"):
        """Write the contents of this instance to `path`."""
        data = asdict(self)
        Pathier(path).dumps(data)
