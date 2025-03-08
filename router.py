from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from schemas import STaskAdd, STask
from repository import TaskRepository

router = APIRouter(
	prefix="/tasks",
	tags=["Таски"]
)

# создаем таску
@router.post("")
async def add_task( 
	task: Annotated[STaskAdd, Depends()],
):
	task_id = await TaskRepository.add_one(task)
	return {"task_id": task_id}

# читаем таску
@router.get("")
async def get_tasks() -> list[STask]:
	tasks = await TaskRepository.find_all()
	return tasks



# обновляем таску	
@router.put("/{task_id}")
async def update_task(
	task_id: int,
	task: Annotated[STaskAdd, Depends()],
):
	try:
		task_id = await TaskRepository.update_one(task_id, task)
		return {"task_id": task_id}
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))

# удаляем таску
@router.delete("/{task_id}")
async def delete_task(task_id: int):
	try:
		task_id = await TaskRepository.delete_one(task_id)
		return {"task_id": task_id}
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))