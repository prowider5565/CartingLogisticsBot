import logging


logger = logging.getLogger(__name__)


async def locale(state):
    data = await state.get_data()
    logger.info("______________________________")
    logger.info(f"Current data: {data}")
    return data["lang"]
