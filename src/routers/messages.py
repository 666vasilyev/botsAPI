from fastapi import APIRouter
from src.core.celery.celery_tasks import sync_celery_post_messages
from src.models import MessagesPostResModel, TaskIdModel

router = APIRouter(prefix="/message")


@router.post("/", response_model=TaskIdModel)
async def post_messages(collect_model: MessagesPostResModel):
    celery_task = sync_celery_post_messages.delay(collect_model.dict())
    return celery_task.id
