from fastapi import APIRouter

from src.core.celery import celery_tasks
from src.models import AllTasksGetReqModel, TaskGetReqModel

router = APIRouter(prefix="/task")


@router.get("/{task_id}")
async def get_task_by_id(task_id: str):
    task = celery_tasks.celery.AsyncResult(task_id)
    task_status = task.status
    task_result = celery_tasks.redis.get(task_id)
    return TaskGetReqModel(
        task_id=task_id, task_status=task_status, task_result=task_result
    )


@router.get("/")
async def get_tasks():
    keys = celery_tasks.redis.keys("celery-task-meta-*")

    task_ids = [key.decode("utf-8").split("-", 3)[-1] for key in keys]

    tasks = []
    for task_id in task_ids:
        task = await get_task_by_id(task_id)
        tasks.append(task)

    return AllTasksGetReqModel(tasks=tasks)
