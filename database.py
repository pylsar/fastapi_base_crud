from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Optional

engine = create_async_engine(
	"sqlite+aiosqlite:///tasks.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
	pass

class TaskOrm(Model):
	__tablename__ = "tasks"
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	description: Mapped[Optional[str]]
	is_completed: Mapped[bool] = mapped_column(default=False)


# Создаем таблицу (взято из доки sqlalchemy)
async def create_tables():
	async with engine.begin() as conn:
		await conn.run_sync(Model.metadata.create_all)	


# Удаляем таблицу (нужно на этапе разработки)
async def delete_tables():
	async with engine.begin() as conn:
		await conn.run_sync(Model.metadata.drop_all)			