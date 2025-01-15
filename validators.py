import re
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user_crud, city_crud


async def check_user_name_duplicate(
        name: str,
        session: AsyncSession, ) -> None:
    user_id = await user_crud.get_user_id_by_name(name, session)
    if user_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким именем уже существует!',
        )


async def check_city_name_duplicate(
        name: str,
        session: AsyncSession, ) -> None:
    city_id = await city_crud.get_city_id_by_name(name, session)
    if city_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Место с таким именем уже существует!',
        )


async def check_city_exists(
        name: str,
        session: AsyncSession, ) -> None:
    city_id = await city_crud.get_city_id_by_name(name, session)
    if city_id is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Места с таким именем не существует!',
        )


async def check_time(time: str):
    if not re.fullmatch(r"^([01]\d|2[0-3])$", time):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Время должно быть в формате '00'–'23'."
        )
    return True
