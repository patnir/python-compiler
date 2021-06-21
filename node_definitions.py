import dataclasses
from typing import Union, List


@dataclasses.dataclass
class IntegerNode:
    value: int


@dataclasses.dataclass
class VarRef:
    value: str


@dataclasses.dataclass
class CallNode:
    name: str
    arg_expressions: Union[List[str], List[VarRef], List[int]]


@dataclasses.dataclass
class DefNode:
    name: str
    arg_names: List[str]
    body: Union[IntegerNode, CallNode, VarRef]
