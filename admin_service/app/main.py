import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from database import database as database
from database.database import Task
from model.task import TaskModel

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/tasks")
def get_tasks(db: db_dependency):
    tasks = db.query(Task).all()
    return tasks


@app.get("/get_task_by_id")
def get_task_by_id(task_id: int, db: db_dependency):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/create_task")
def create_task(task: TaskModel, db: db_dependency):
    db_task = Task(id=task.id, time=task.time, text=task.text)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/delete_task")
def delete_task(task_id: int, db: db_dependency):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
