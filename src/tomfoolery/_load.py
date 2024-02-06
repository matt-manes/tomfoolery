@classmethod
def load(cls, path: Pathish = Pathier(__file__).parent / "filepath") -> Self:
    """Return an instance of this class populated from `path`."""
    data = Pathier(path).loads()
    return dacite.from_dict(cls, data)
