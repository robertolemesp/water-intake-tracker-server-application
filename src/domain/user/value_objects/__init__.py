from pydantic import EmailStr, ValidationError

class Email:
  def __init__(self, email: str):
    try:
      validEmail = EmailStr(email)
      self.value = str(validEmail)
    except ValidationError:
      raise ValueError(f'Invalid email address: {email}')

  def __str__(self):
    return self.value

  def __repr__(self):
    return f'Email({self.value!r})'

  def __eq__(self, other):
    return isinstance(other, Email) and self.value == other.value

  def __hash__(self):
    return hash(self.value)
