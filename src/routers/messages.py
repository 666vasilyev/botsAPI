from fastapi import APIRouter

from src.core.celery import celery_tasks
from src.models import MessagesPostResModel, TaskIdModel

router = APIRouter(prefix="/message")


@router.post("/", response_model=TaskIdModel)
async def post_messages(collect_model: MessagesPostResModel):
    celery_task = celery_tasks.sync_celery_post_messages.delay(collect_model.dict())
    return TaskIdModel(task_id=celery_task.id)
