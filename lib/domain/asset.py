import dataclasses


@dataclasses.dataclass
class Asset:
    name: str
    ticker: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
