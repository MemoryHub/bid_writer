from pydantic import BaseModel
from typing import Any, List, Optional

class ResponseModel(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None 