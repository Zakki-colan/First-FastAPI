from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def create_task(
    db: Session,
    task: schemas.TaskCreate,
) -> models.Task:
    db_task = models.Task(**task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_task(
    db: Session,
    task_id: int,
) -> models.Task | None:
    return db.get(models.Task, task_id)


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[models.Task]:
    statement = (
        select(models.Task)
        .order_by(models.Task.id.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def update_task(
    db: Session,
    db_task: models.Task,
    task_data: schemas.TaskUpdate,
) -> models.Task:
    updates = task_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(
    db: Session,
    db_task: models.Task,
) -> None:
    db.delete(db_task)
    db.commit()