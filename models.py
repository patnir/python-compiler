import dataclasses


@dataclasses.dataclass
class Token:
    token_type: str
    value: str
