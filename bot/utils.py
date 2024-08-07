import logging


logger = logging.getLogger(__name__)


async def locale(state):
    data = await state.get_data()
    return data["lang"]
