from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import city_crud


async def check_city_name_duplicate(
        name: str,
        session: AsyncSession) -> None:
    """Проверка на дублирование имени места."""
    city_id: int or None = await city_crud.get_city_id_by_name(name, session)
    if city_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Место с таким именем уже существует!',
        )


async def check_city_exists(
        name: str,
        session: AsyncSession) -> None:
    """Проверка существования места."""
    city_id: int or None = await city_crud.get_city_id_by_name(name, session)
    if city_id is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Места с таким именем не существует!',
        )


async def check_time(time: int) -> None:
    """Проверка корректности времени (0-23)."""
    if not (0 <= time <= 23):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Время должно быть в диапазоне от 0 до 23.'
        )
