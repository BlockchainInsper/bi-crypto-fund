import dataclasses

@dataclasses.dataclass
class Transaction:
    asset_id: str
    weight: float
    timestamp: int
    added_by: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)