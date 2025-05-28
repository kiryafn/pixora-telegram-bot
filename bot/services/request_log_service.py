from bot.models import RequestLog
from bot.repositories import RequestLogRepository, request_log_repository
from bot.repositories import UserRepository, user_repository
from bot.services import BaseService


class RequestLogService(BaseService[RequestLog]):
    """
    Service layer for managing RequestLog entities.

    Ensures that request logs are only saved if the associated user exists.

    Attributes:
        user_repository (UserRepository): Repository used for validating user existence.
    """

    def __init__(self, repository: RequestLogRepository, user_repository: UserRepository) -> None:
        """
        Initializes the RequestLogService with required repositories.

        Args:
            repository (RequestLogRepository): The repository for request logs.
            user_repository (UserRepository): The repository for user validation.
        """
        super().__init__(repository)
        self.user_repository = user_repository

    async def save(self, request: RequestLog) -> RequestLog:
        """
        Saves a request log if the referenced user exists.

        Args:
            request (RequestLog): The request log to be saved.

        Raises:
            Exception: If the user associated with the request does not exist.
            # TODO: Replace generic Exception with a custom exception.

        Returns:
            RequestLog: The saved request log.
        """
        user = await self.user_repository.get_by_id(request.user_id)
        if not user:
            raise Exception(f"User {request.user_id} not found")

        return await self.repository.save(request)


# Singleton instance for accessing request log logic
request_log_service = RequestLogService(request_log_repository, user_repository)