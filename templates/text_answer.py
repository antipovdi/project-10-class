from aiogram.types import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder

async def obj_media_group(data: dict) -> list[InputMediaPhoto]:
    txt = await obj_text(data)
    album_builder = MediaGroupBuilder()
    for i in data['photos']:
        album_builder.add_photo(media=i)
    return album_builder.build()


async def obj_text(data: dict) -> str:
    return (f"Название: {data['title']} \n\n"
            f"Описание: {data['describe']} \n\n"
            f"Текущая цена: {data['cost']}\n\n"
            f"Начало: {data['start']}\n"
            f"Конец: {data['end']}\n\n"
            f"Владелец: tg://user?id={data['owner']}\n")
