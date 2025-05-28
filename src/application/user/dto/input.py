from dataclasses import dataclass

@dataclass
class CreateUserInput:
    name: str
    email: str
    weight_kg: float

