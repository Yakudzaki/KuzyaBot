from loguru import logger


async def errors_handler(update, exception):
    logger.exception(exception)
    logger.debug(update)

    return True