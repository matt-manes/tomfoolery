import sys

import ast_comments as ast  # type: ignore
import pytest
from pathier import Pathier

from tomfoolery import TomFoolery, generate_from_file

root = Pathier(__file__).parent


def test__engine():
    datafile = root / "venue.toml"
    pyfile = datafile.with_suffix(".py")
    pyfile.delete()
    generate_from_file(datafile, pyfile)
    assert pyfile.exists()


def test__dataclass():
    root.add_to_PATH()
    from venue import Venue

    venue = Venue.load()
    venuetoml = (root / "venue.toml").loads()
    assert venue.name == venuetoml["name"]
    assert venue.address.city == venuetoml["address"]["city"]
    assert type(venue.calendar.num_events) == int


def test__no_overwrite():
    datafile = root / "venue.toml"
    src = (root / "venue2.py").read_text()
    module = ast.parse(src)  # type:ignore
    engine = TomFoolery(module)  # type:ignore
    tom = engine.generate(datafile.stem, datafile.loads())
    (root / "venue22.py").write_text(tom)
    assert src == tom


def test__update():
    datafile = root / "venue.toml"
    data = datafile.loads()
    original = datafile.loads()
    data["yee"] = "haw"
    data["afraid_of_the_dark"] = {"me": False, "you": True}
    datafile.dumps(data)
    generate_from_file(datafile)
    try:
        sys.modules.pop("venue")
    except Exception as e:
        pass
    from venue import Venue

    venue = Venue.load()
    venuetoml = (root / "venue.toml").loads()
    assert venue.name == venuetoml["name"]
    assert venue.address.city == venuetoml["address"]["city"]
    assert venue.yee == "haw"
    assert not venue.afraid_of_the_dark.me
    assert venue.afraid_of_the_dark.you
    datafile.dumps(original)


def test__no_recursion():
    datafile = root / "venue.toml"
    pyfile = datafile.with_name("no_recursion.py")
    pyfile.delete()
    generate_from_file(datafile, pyfile, False)
    pyfile.add_to_PATH()
    from no_recursion import Venue

    venue = Venue.load()
    assert isinstance(venue.name, str)
    assert isinstance(venue.address, dict)
    assert isinstance(venue.calendar, dict)
