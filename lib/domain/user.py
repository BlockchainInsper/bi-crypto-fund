import dataclasses

@dataclasses.dataclass
class User:
    username: str
    password_hash: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)