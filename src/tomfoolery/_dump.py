def dump(self, path: Pathish = Pathier(__file__).parent / "filepath"):
    """Write the contents of this `datamodel` object to `path`."""
    data = asdict(self)
    Pathier(path).dumps(data)
