from dataclasses import dataclass

@dataclass
class CreateUserOutput:
    id: str
    name: str
    email: str
    weightKg: float
    dailyGoalMl: float
