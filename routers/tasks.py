from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    return crud.create_task(db, task)


@router.get(
    "/",
    response_model=list[schemas.TaskResponse],
)
def read_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_tasks(db, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse,
)
def edit_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return crud.update_task(db, task, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    crud.delete_task(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)