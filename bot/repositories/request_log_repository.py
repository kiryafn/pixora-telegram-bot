from bot.models import RequestLog
from bot.repositories import BaseRepository


class RequestLogRepository(BaseRepository[RequestLog]):
    """
    Repository for managing RequestLog entities.

    Inherits standard CRUD operations from BaseRepository.
    Can be extended with custom analytics or filtering methods in the future.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the RequestLog model.
        """
        super().__init__(RequestLog)


# Singleton instance for accessing request logs
request_log_repository = RequestLogRepository()