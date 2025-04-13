from sqlalchemy import select

from database import new_session, TaskOrm
from schemas import STaskAdd, STask


class TaskRepository:
	@classmethod
	async def add_one(cls, data:STaskAdd) -> int:
		async with new_session() as session:
			task_dict = data.model_dump()
			task = TaskOrm(**task_dict)
			session.add(task)
			await session.flush()
			await session.commit()
			return task.id

	@classmethod
	async def find_all(cls)  -> list[STask]:
		async with new_session() as session:
			query = select(TaskOrm)
			result = await session.execute(query)
			task_models = result.scalars().all()
			 # Преобразуем TaskOrm в словарь и валидируем с помощью STask
			task_schemas = [
				STask.model_validate({
					"id": task_model.id,
					"name": task_model.name,
					"description": task_model.description
				})
				for task_model in task_models
			]
			return task_schemas



# обновляем
	@classmethod
	async def update_one(cls, task_id: int, data: STaskAdd) -> int:
		async with new_session() as session:
			# Находим задачу по id
			query = select(TaskOrm).where(TaskOrm.id == task_id)
			result = await session.execute(query)
			task = result.scalars().first()

			if not task:
				raise ValueError("Task not found")

			# Обновляем данные задачи
			task.name = data.name
			task.description = data.description
			# task.is_completed = data.is_completed

			await session.commit()
			return task_id	
		
# обновлем завершеность
	@classmethod
	async def toggle_completion(cls, task_id: int) -> int:
		async with new_session() as session:
			query = select(TaskOrm).where(TaskOrm.id == task_id)
			result = await session.execute(query)
			task = result.scalars().first()

			if not task:
				raise ValueError("Task not found")

			# Переключаем статус
			task.is_completed = not task.is_completed
			await session.commit()
			return task_id			

# удаляем
	@classmethod
	async def delete_one(cls, task_id: int) -> int:
		async with new_session() as session:
			# Находим задачу по id
			query = select(TaskOrm).where(TaskOrm.id == task_id)
			result = await session.execute(query)
			task = result.scalars().first()

			if not task:
				raise ValueError("Task not found")

			# Удаляем задачу
			await session.delete(task)
			await session.commit()
			return task_id			