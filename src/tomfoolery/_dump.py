def dump(self, path: Pathish = Pathier(__file__).parent / "filepath"):
    """Write the contents of this instance to `path`."""
    data = asdict(self)
    Pathier(path).dumps(data)
