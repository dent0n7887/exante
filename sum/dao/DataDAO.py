from consts import DB_SESSION
from models import DataModel
from sqlalchemy.future import select
from typing import Any, List


class DataDAO:
    def __init__(self, app):
        self._app = app

    async def create(self, js: Any, sum: int) -> DataModel:
        async with self._app[DB_SESSION]() as session:
            data_model = DataModel(js=js, sum=sum)
            session.add(data_model)
            await session.commit()

            return data_model

    async def get_by_sum(self, sum: int) -> List[DataModel]:
        async with self._app[DB_SESSION]() as session:
            data_models = await session.execute(select(DataModel).filter(DataModel.sum == sum))
            data_models = data_models.scalars().all()

            return data_models
