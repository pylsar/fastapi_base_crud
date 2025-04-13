from pydantic import BaseModel
from typing import Optional

class STaskAdd(BaseModel):
	name: Optional[str] = None
	description: Optional[str] = None	
	is_completed: bool = False

class STask(STaskAdd):
	id: int