from bot.models.request_log import RequestLog
from bot.repositories.request_log_repository import RequestLogRepository, request_log_repository
from bot.services import BaseService


class RequestLogService(BaseService[RequestLog]):
    def __init__(self, repository: RequestLogRepository) -> None:
        super().__init__(repository)

request_log_service = RequestLogService(request_log_repository)
