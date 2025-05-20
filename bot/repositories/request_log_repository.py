from bot.models.request_log import RequestLog
from bot.repositories import BaseRepository


class RequestLogRepository(BaseRepository[RequestLog]):
    def __init__(self) -> None:
        super().__init__(RequestLog)

request_log_repository = RequestLogRepository()