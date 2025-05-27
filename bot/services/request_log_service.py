from bot.models import RequestLog
from bot.repositories import RequestLogRepository, request_log_repository
from bot.repositories import UserRepository, user_repository
from bot.services import BaseService


class RequestLogService(BaseService[RequestLog]):
    def __init__(self, repository: RequestLogRepository, user_repository: UserRepository) -> None:
        super().__init__(repository)
        self.user_repository = user_repository

    async def save(self, request: RequestLog) -> RequestLog:
        user = await user_repository.get_by_id(request.user_id)
        if not user:
            raise Exception(f"User {request.user_id} not found")

        return await self.repository.save(request)


request_log_service = RequestLogService(request_log_repository, user_repository)
