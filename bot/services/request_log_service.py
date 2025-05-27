from bot.models.request_log import RequestLog
from bot.repositories.request_log_repository import RequestLogRepository, request_log_repository
from bot.repositories.user_repository import UserRepository, user_repository
from bot.services import BaseService


class RequestLogService(BaseService[RequestLog]):
    def __init__(self, repository: RequestLogRepository, user_repository: UserRepository) -> None:
        super().__init__(repository)
        self.user_repository = user_repository

    async def save(self, request: RequestLog) -> None:
        user = await user_repository.get_by_id(request.user_id)
        if not user:
            raise Exception(f"User {request.user_id} not found")

        await self.repository.save(request)


request_log_service = RequestLogService(request_log_repository, user_repository)
