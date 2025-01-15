from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, City


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


class CRUDUser(CRUDBase):

    async def get_user_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        user_id = await session.execute(
            select(User.id).where(User.name == name)
        )
        return user_id.scalars().first()


class CRUDCity(CRUDBase):

    async def get_city_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        city_id = await session.execute(
            select(City.id).where(City.name == name)
        )
        return city_id.scalars().first()

    async def get_city_obj_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        city = await session.execute(
            select(City).where(City.name == name)
        )
        return city.scalars().first()


city_crud = CRUDCity(City)
user_crud = CRUDUser(User)
