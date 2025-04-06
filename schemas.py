from pydantic import BaseModel
from typing import Optional

class STaskAdd(BaseModel):
	name: str
	description: Optional[str] = None	
	is_completed: bool = False

class STask(STaskAdd):
	id: int