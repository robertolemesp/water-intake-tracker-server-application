class DomainError(ValueError):
  """Base class for domain errors"""
  pass

class DomainNotFoundError(DomainError):
  """404 — Resource not found"""
  def __init__(self, resource: str, identifier: str | int):
    message = f"{resource} with identifier '{identifier}' was not found."
    super().__init__(message)

class DomainConflictError(DomainError):
  """409 — Resource conflict"""
  def __init__(self, resource: str, reason: str = 'Conflict occurred'):
    message = f'Conflict with {resource}: {reason}.'
    super().__init__(message)

class DomainBadRequestError(DomainError):
  """400 — Bad request — invalid operations"""
  def __init__(self, detail: str):
    message = f'Bad request: {detail}.'
    super().__init__(message)
