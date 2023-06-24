import pytest

from tomfoolery import TomFoolery
from pathier import Pathier

root = Pathier(__file__).parent


def test__engine():
    (root / "venue.py").write_text("")
    engine = TomFoolery()
    engine.generate_from_file(root / "venue.toml", True)
    assert (root / "venue.py").exists()


def test__dataclass():
    root.add_to_PATH()
    from venue import Venue

    venue = Venue.load()
    venuetoml = (root / "venue.toml").loads()
    assert venue.name == venuetoml["name"]
    assert venue.address.city == venuetoml["address"]["city"]
    assert type(venue.calendar.num_events) == int
    # (root / "venue.py").write_text("")
