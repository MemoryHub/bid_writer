from pydantic import BaseModel
from typing import Any, List, Optional

class ResponseModel(BaseModel):
    message: str
    data: Optional[Any] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None 