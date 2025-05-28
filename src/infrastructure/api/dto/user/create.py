from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
  name: str
  email: EmailStr
  weightKg: float


class CreateUserResponse(BaseModel):
  id: str
  name: str
  email: str
  dailyGoalMl: float
  weightKg: float
