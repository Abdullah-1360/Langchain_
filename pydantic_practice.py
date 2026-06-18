from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Annotated, List, Optional

class User(BaseModel):
    id: int
    name: str
    email: Annotated[str, Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="A valid email address")]
    signup_date: datetime
# Example of creating a User instance

try:
    user_data = User(
        id=1,
        name="Alice",
        email="alice@com",
        signup_date="2024-06-01T12:00:00"
    )
except ValidationError as e:
        print(f"Validation error: {e}")
print(user_data)
