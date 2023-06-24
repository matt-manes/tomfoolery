@classmethod
def load(cls, path: Pathish = Pathier(__file__).parent / "filepath") -> Self:
    """Return a `datamodel` object populated from `path`."""
    data = Pathier(path).loads()
    return dacite.from_dict(cls, data)
