from fastapi import APIRouter
<<<<<<< HEAD
from src.core.celery.celery_tasks import sync_celery_post_messages
=======

from src.core.celery import celery_tasks
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
from src.models import MessagesPostResModel, TaskIdModel

router = APIRouter(prefix="/message")


@router.post("/", response_model=TaskIdModel)
async def post_messages(collect_model: MessagesPostResModel):
<<<<<<< HEAD
    celery_task = sync_celery_post_messages.delay(collect_model.dict())
    return celery_task.id
=======
    celery_task = celery_tasks.sync_celery_post_messages.delay(collect_model.dict())
    return TaskIdModel(task_id=celery_task.id)
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
