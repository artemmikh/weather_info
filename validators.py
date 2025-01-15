from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user_crud


async def check_user_name_duplicate(
        name: str,
        session: AsyncSession, ) -> None:
    user_id = await user_crud.get_user_id_by_name(name, session)
    if user_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким именем уже существует!',
        )
