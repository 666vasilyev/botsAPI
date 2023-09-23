from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette_admin.views import CustomView

from src.models import MessagesPostResModel
from src.routers.messages import post_messages
from typing import List, Any

from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from starlette_admin import action
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import ActionFailed


# Создаем view-модель
class ChannelTestingView(CustomView):
    def __init__(self):
        super().__init__(label='Testing', path='/channel/testing', template_path="create.html")
        
        # Добавляем поля во view-модель
        # self.add_field("bot_id", str)
        # self.add_field("channel_id", str)
        # self.add_field("message", str)

        # Добавляем кнопку "Post"
        # self.add_action_button("Post", self.post_message)

    async def render(self, request: Request, templates: Jinja2Templates) -> Response:
        print(templates.env.list_templates())
        return await super().render(request, templates)

    async def post_message(self):
        # Получаем значения полей из view-модели
        bot_id = self.get_field_value("bot_id")
        channel_id = self.get_field_value("channel_id")
        message = self.get_field_value("message")

        # Создаем экземпляр модели данных для post-запроса
        post_data = MessagesPostResModel(bot_id=bot_id, channel_id=channel_id, message=message)

        # Выполняем post-запрос или вызываем функцию
        # async def post_messages(collect_model: MessagesPostResModel)
        # celery_task = celery_tasks.sync_celery_post_messages.delay(collect_model.dict())
        # return TaskIdModel(task_id=celery_task.id)
        # Вместо этого места вставьте ваш код для обработки post-запроса

        await post_messages(collect_model=post_data)

        # Возвращаем результат обработки
        return "Post request executed successfully"
    

class ArticleView(ModelView):
    actions = ["testing", "delete"] # `delete` function is added by default

    @action(
        name="testing",
        text="Testing",
        submit_btn_text="Yes, proceed",
        submit_btn_class="btn-success",
        form="""
        <form>
            <div class="mt-3">
                <input type="text" class="form-control" name="example-text-input" placeholder="Enter value">
            </div>
        </form>
        """,
    )
    async def make_published_action(self, request: Request, pks: List[Any]) -> str:
        # Write your logic here

        data: FormData = await request.form()
        user_input = data.get("example-text-input")

        print(data)
        # Display successfully message
        return "{} articles were successfully marked as published".format(len(pks))
