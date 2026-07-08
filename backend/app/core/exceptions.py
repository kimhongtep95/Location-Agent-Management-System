class LamsError(Exception):
    """Base application exception."""


class AuthenticationError(LamsError):
    """Raised for authentication or authorization failures."""


class EntityNotFoundError(LamsError):
    """Raised when an entity cannot be found."""


class ValidationError(LamsError):
    """Raised when business validation fails."""
