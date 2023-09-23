<<<<<<< HEAD
from .bots import router as bot_router
from .channels import router as channel_router
from .tasks import router as task_router
from .messages import router as messages_router
=======
from .bots.v1 import router as bot_router
from .channels import router as channel_router
from .messages import router as messages_router
from .tasks import router as task_router
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
