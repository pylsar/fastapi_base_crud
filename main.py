from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables, delete_tables
from router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	# await delete_tables()
	# print("таблица удалена")
	await create_tables()
	print("таблица создана")
	yield
	print("Выключено")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL вашего Vue-приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



