import dataclasses

@dataclasses.dataclass
class Transaction:
    asset_id: str
    weight: float
    timestamp: int

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)