from fastapi import APIRouter

<<<<<<< HEAD
from src.core.celery.celery_tasks import celery, redis
from src.models import (
    TaskGetReqModel,
    AllTasksGetReqModel,
)
=======
from src.core.celery import celery_tasks
from src.models import AllTasksGetReqModel, TaskGetReqModel
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)

router = APIRouter(prefix="/task")


@router.get("/{task_id}")
async def get_task_by_id(task_id: str):
<<<<<<< HEAD
    task = celery.AsyncResult(task_id)
    task_status = task.status
    task_result = redis.get(task_id)
=======
    task = celery_tasks.celery.AsyncResult(task_id)
    task_status = task.status
    task_result = celery_tasks.redis.get(task_id)
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
    return TaskGetReqModel(
        task_id=task_id, task_status=task_status, task_result=task_result
    )


@router.get("/")
async def get_tasks():
<<<<<<< HEAD
    keys = redis.keys("celery-task-meta-*")
=======
    keys = celery_tasks.redis.keys("celery-task-meta-*")
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)

    task_ids = [key.decode("utf-8").split("-", 3)[-1] for key in keys]

    tasks = []
    for task_id in task_ids:
        task = await get_task_by_id(task_id)
        tasks.append(task)

    return AllTasksGetReqModel(tasks=tasks)
