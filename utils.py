from aiogram.dispatcher import FSMContext


async def get_from_context(state: FSMContext, key: str) -> set:
    async with state.proxy() as data:
        result = data.get(key)
        return set(result) if result else ()


def parse_text(text: str, delimiter=" "):
    return text.split(delimiter)
